import numpy

class PLPhoto(object):

    def __init__(self, url=None, image=None):

        self._image = image
        self._url = url

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def image(self):
        if self._image is None: self.load()
        return self._image

    def load(self):
        import matplotlib.image as mpimg
        self._image = numpy.array(mpimg.imread(self._url))

    def show(self, image=None, show=True):
        import matplotlib.pyplot as plt
        cmap = 'gray'
        fig, ax = plt.subplots()
        if image is None:
            ax.imshow(self.image(),cmap=cmap)
        else:
            ax.imshow(image,cmap=cmap)
        ax.set_xticks([], minor=False)
        ax.set_yticks([], minor=False)
        if show: plt.show()
        return fig, ax

    def nchannels(self):
        s = numpy.array(self.image().shape)
        if s.size == 2:
            return 1
        else:
            return s[2]

    def get_channel(self, channel=0):
        if self.nchannels() > 1:
            return self.image()[:,:,channel]
        else:
            return self.image()

    def info(self):
        txt = ""
        txt += "\nurl:         %s " % self.get_url()
        if self.image() is None:
            txt += "\nimage:     None"
        else:
            txt += "\nimage:       " + repr(self.image().shape)

        txt += "\nchannels:    %d" % self.nchannels()
        return txt

    # def grayscale(rgb):
    #     return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])

    def grayscale(self, r=0.299, g=0.587, b=0.114):
        tot = r+g+b
        if tot == 0: tot=1
        return numpy.dot(self.image()[...,:3], [r/tot, g/tot, b/tot])

    def to_python_code(self):
        txt = "from orangecontrib.photolab.util.photolab_objects import PLPhoto"
        txt += "\nplimg_in = PLPhoto(url='%s')" % self.get_url()
        return txt

class PLFilter(object):
    def __init__(self):
        self._name = ""
        self._username = ""
        self._input_names = None
        self._input_values = None

    def get_input_values(self):
        return self._input_values

    def get_input_names(self):
        return self._input_names

    def get_name(self):
        return self._name

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username



    def grayscale_apply(self, pl_image):
        r, g, b = self.get_input_values()
        image =  numpy.dot(pl_image.image()[..., :3], [r, g, b])
        return PLPhoto(image=image)

    def grayscale_set(self, r=0.299, g=0.587, b=0.114):
        self._input_names = ['r', 'g', 'b']
        tot = r + g + b
        if tot == 0: tot = 1
        self._input_values = [r/tot, g/tot, b/tot]
        self._name = "grayscale"

    @classmethod
    def grayscale(cls, pl_image, r=0.299, g=0.587, b=0.114):
        f = PLFilter()
        f.grayscale_set(r=r, g=g, b=b)
        return f.grayscale_apply(pl_image)

    def to_python_code(self):
        txt = "\n\nfrom orangecontrib.photolab.util.photolab_objects import PLFilter"
        if self.get_name() == "grayscale":
            txt += "\nplimg_out = PLFilter.grayscale(plimg_in, %g, %g, %g)" % \
                   (tuple(self.get_input_values()))

        return txt


if __name__ == "__main__":
    from srxraylib.plot.gol import set_qt
    set_qt()


    pl1 = PLPhoto(url="/Users/srio/Public/ines/DSC_2863.jpg")

    print(pl1.info())
    pl1.show()



    fil1 = PLFilter()
    fil1.grayscale_set()
    pl2 = fil1.grayscale_apply(pl1)

    pl2.show()


    txt_code = pl1.to_python_code()
    txt_code += fil1.to_python_code()

    print(txt_code)

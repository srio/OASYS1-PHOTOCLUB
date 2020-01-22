
import os
import numpy

from PyQt5.QtWidgets import QMessageBox

from orangewidget import gui, widget
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from orangewidget import gui as orangegui


import matplotlib.image as mpimg


class OWFileReader(widget.OWWidget):
    name = "File reader"
    description = "File reader (using matplotlib)"
    icon = "icons/image_file_reader.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "msanchezdelrio@gmail.com"
    priority = 5
    category = "Tools"
    keywords = ["data", "view"]

    outputs = [{"name": "image",
                "type": numpy.ndarray,
                "doc": "numpy array with image",
                "id": "image"},
               ]

    want_main_area = 0

    filename = Setting("")



    def __init__(self):
        super().__init__()

        self.runaction = widget.OWAction("Read image [jpeg] File", self)
        self.runaction.triggered.connect(self.read_file)
        self.addAction(self.runaction)

        self.setFixedWidth(590)
        self.setFixedHeight(150)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "Image File Selection", addSpace=True, orientation="vertical",
                                         width=570, height=70)

        figure_box = oasysgui.widgetBox(left_box_1, "", addSpace=True, orientation="horizontal", width=550, height=35)

        self.le_beam_file_name = oasysgui.lineEdit(figure_box, self, "filename", "Image File Name",
                                                    labelWidth=120, valueType=str, orientation="horizontal")
        self.le_beam_file_name.setFixedWidth(330)

        gui.button(figure_box, self, "...", callback=self.selectFile)

        #gui.separator(left_box_1, height=20)

        button = gui.button(self.controlArea, self, "Read Image File", callback=self.read_file)
        button.setFixedHeight(45)

        gui.rubber(self.controlArea)

    def selectFile(self):
        self.le_beam_file_name.setText(oasysgui.selectFileFromDialog(self, self.filename, "Open Image File"))

    def load_file_to_numpy_array(self):
        self.current_image = mpimg.imread(self.filename)

    def read_file(self):
        self.setStatusMessage("")
        filename = self.le_beam_file_name.text()
        if not os.path.exists(filename):
            raise Exception("File not found %s"%filename)

        try:
            if congruence.checkFileName(filename):

                try:
                    self.load_file_to_numpy_array()
                except:
                    raise FileExistsError("Error loading imagefile: %s"%filename)

        except:
            raise Exception("Failed to read file %s"%filename)

        self.send("image", self.current_image)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    a = QApplication(sys.argv)
    ow = OWFileReader()

    ow.filename = "/Users/srio/Public/ines/DSC_1575.jpg"

    ow.show()
    a.exec_()

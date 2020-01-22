import numpy

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import widget
import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

# import matplotlib.pyplot as plt
import matplotlib
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from srxraylib.plot.gol import plot_image


class OWSketch(widget.OWWidget):
    name = "Sketch"
    description = "Sketch"
    icon = "icons/sketch.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "msanchezdelrio@gmail.com"
    priority = 10
    category = "Filters"
    keywords = ["data", "view"]

    want_main_area = 1

    inputs = [("image", numpy.ndarray, "set_input")]

    outputs = [{"name": "image",
                "type": numpy.ndarray,
                "doc": "numpy array with image",
                "id": "image"},
               ]

    want_main_area=1

    MAX_WIDTH = 1320
    MAX_HEIGHT = 700

    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560
    TABS_AREA_WIDTH = MAX_WIDTH - CONTROL_AREA_WIDTH

    show_axes = Setting(0)
    show_colormap = Setting(0)
    show_info = Setting(0)

    current_image = None

    def __init__(self):
        super().__init__()

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        # CONTROL AREA
        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        general_options_box = oasysgui.widgetBox(self.controlArea, "General Options", addSpace=True, orientation="vertical", width=400)


        gui.button(general_options_box, self, "View/Refresh", callback=self.run_action, height=45)

        gui.separator(general_options_box)


        # gui.comboBox(general_options_box, self, "show_axes", label="Show axes",labelWidth=220,
        #                              items=["No","Yes"],
        #                              sendSelectedValue=False, orientation="horizontal",
        #                              callback=self.view)
        #
        # gui.separator(general_options_box)
        #
        # gui.comboBox(general_options_box, self, "show_colormap", label="Show colormap",labelWidth=220,
        #                              items=["No","Yes"],
        #                              sendSelectedValue=False, orientation="horizontal",
        #                              callback=self.view)
        #
        # gui.comboBox(general_options_box, self, "show_info", label="Show info",labelWidth=220,
        #                              items=["No","Yes"],
        #                              sendSelectedValue=False, orientation="horizontal",
        #                              callback=self.view)

        gui.separator(general_options_box)

        # MAIN AREA


        tabs_setting = oasysgui.tabWidget(self.mainArea)

        tmp = oasysgui.createTabPage(tabs_setting, "View")
        self.view_id = gui.widgetBox(tmp, "", addSpace=True, orientation="vertical")
        self.view_id.setFixedHeight(self.TABS_AREA_HEIGHT - 30)
        self.view_id.setFixedWidth(self.TABS_AREA_WIDTH - 20)

        tmp = oasysgui.createTabPage(tabs_setting, "Info")
        self.info_id = oasysgui.textArea() #height=self.IMAGE_HEIGHT-35)
        info_box = oasysgui.widgetBox(tmp, "", addSpace=True, orientation="horizontal") #, height = self.IMAGE_HEIGHT-20, width = self.IMAGE_WIDTH-20)
        info_box.layout().addWidget(self.info_id)


    def run_action(self):
        # if ConfirmDialog.confirmed(self):
        self.view()
        self.send("image", self.current_image)

    def set_input(self, input_data):
        if input_data is not None:
            self.current_image = input_data
            self.run_action()

    def view(self):
        cmap = "hot"
        cmap = 'nipy_spectral'

        if self.current_image is None:
            raise Exception("Please load an image....")

        f = Figure()
        # A canvas must be manually attached to the figure (pyplot would automatically
        # do it).  This is done by instantiating the canvas with the figure as
        # argument.
        figure_canvas = FigureCanvasQTAgg(f)
        toolbar = NavigationToolbar(figure_canvas, self)
        # gs1 = matplotlib.gridspec.GridSpec(2, 1)
        ax = f.add_subplot(111)
        ax.imshow(self.current_image[:,:,:])

        # gs1.tight_layout(f, rect=[0.01, 0.01, 0.99, 0.99], h_pad=0.005)
        # matplotlib.tight_layout.auto_adjust_subplotpars(f, renderer=,
        #                                                 nrows_ncols=(10, 1)), 'num1num2_list', and 'subplot_list)




        # #
        # # triangulation plot
        # #
        # self.triangulation_id.layout().removeItem(self.triangulation_id.layout().itemAt(1))
        # self.triangulation_id.layout().removeItem(self.triangulation_id.layout().itemAt(0))
        #
        # f = self.fea_file_object.plot_triangulation(show=0)
        # figure_canvas = FigureCanvasQTAgg(f)
        # toolbar = NavigationToolbar(figure_canvas, self)
        #
        # self.triangulation_id.layout().addWidget(toolbar)
        # self.triangulation_id.layout().addWidget(figure_canvas)

        # if self.show_info == 1:
        #     ax.set_title(self.filename, fontsize=12)

        if True: #not(self.show_axes):
            ax.set_xticks([], minor=False)
            ax.set_yticks([], minor=False)



        self.view_id.layout().removeItem(self.view_id.layout().itemAt(1))
        self.view_id.layout().removeItem(self.view_id.layout().itemAt(0))
        self.view_id.layout().addWidget(toolbar)
        self.view_id.layout().addWidget(figure_canvas)



if __name__ == "__main__":


    import sys
    from oasys.widgets.exchange import DataExchangeObject
    import matplotlib.image as mpimg

    app = QApplication(sys.argv)
    w = OWSketch()

    w.set_input(mpimg.imread("/Users/srio/Public/ines/DSC_1575.jpg"))
    w.view()

    w.show()

    app.exec()
    w.saveSettings()
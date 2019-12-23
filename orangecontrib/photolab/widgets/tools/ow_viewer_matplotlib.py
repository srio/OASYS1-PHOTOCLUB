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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from srxraylib.plot.gol import plot_image


class OWFileSelector(widget.OWWidget):
    name = "Viewer (matplotlib)"
    description = "Viewer (matplotlib)"
    icon = "icons/viewer_matplotlib.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "msanchezdelrio@gmail.com"
    priority = 20
    category = "Tools"
    keywords = ["data", "view"]

    want_main_area = 1

    inputs = [("filename", str, "set_input"),]

    outputs = [{"name": "filename",
                "type": str,
                "doc": "selected file name",
                "id": "filename"}, ]

    want_main_area=1

    MAX_WIDTH = 1320
    MAX_HEIGHT = 700

    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560
    TABS_AREA_WIDTH = MAX_WIDTH - CONTROL_AREA_WIDTH

    filename = Setting("None")

    show_axes = Setting(0)
    show_colormap = Setting(0)

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

        file_box = oasysgui.widgetBox(general_options_box, "", addSpace=False, orientation="horizontal", height=25)
        self.le_file = oasysgui.lineEdit(file_box, self, "filename", label="Select file", addSpace=False, orientation="horizontal")
        gui.button(file_box, self, "...", callback=self.select_file)

        gui.separator(general_options_box)

        gui.comboBox(general_options_box, self, "show_axes", label="Show axes",labelWidth=220,
                                     items=["No","Yes"],
                                     sendSelectedValue=False, orientation="horizontal")

        gui.separator(general_options_box)

        gui.comboBox(general_options_box, self, "show_colormap", label="Show colormap",labelWidth=220,
                                     items=["No","Yes"],
                                     sendSelectedValue=False, orientation="horizontal")

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



    def select_file(self):
        self.filename = oasysgui.selectFileFromDialog(self, self.filename, "Open File", file_extension_filter="*.*")
        self.le_file.setText(self.filename)

    def run_action(self):
        # if ConfirmDialog.confirmed(self):
        self.view()
        self.send("filename", self.filename)

    def set_input(self, input_data):
        self.filename = input_data
        self.load_file_to_numpy_array()

    def load_file_to_numpy_array(self):
        self.current_image = mpimg.imread(self.filename)

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
        ax = f.add_subplot(111)
        ax.imshow(self.current_image[:,:,:])



        if not(self.show_axes):
            ax.set_xticks([], minor=False)
            ax.set_yticks([], minor=False)
        #
        if self.show_colormap:
            ax2 = f.add_axes([0.9, 0.1, 0.05, 0.7])
            cmap = matplotlib.cm.gray
            norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
            cb1 = matplotlib.colorbar.ColorbarBase(ax2,
                                                   norm=norm,
                                                   cmap=cmap,
                                                   orientation='vertical')


        self.view_id.layout().removeItem(self.view_id.layout().itemAt(0))
        self.view_id.layout().addWidget(figure_canvas)



if __name__ == "__main__":


    import sys
    from oasys.widgets.exchange import DataExchangeObject

    app = QApplication(sys.argv)
    w = OWFileSelector()

    w.filename = "/Users/srio/Desktop/fotos para imprimir/DSC_0293.jpg"
    w.load_file_to_numpy_array()

    w.show()

    app.exec()
    w.saveSettings()
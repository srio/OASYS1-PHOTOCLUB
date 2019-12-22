from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import widget
import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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

    filename = Setting("/Users/srio/Desktop/fotos para imprimir/DSC_0293.jpg")

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


        file_box = oasysgui.widgetBox(general_options_box, "", addSpace=False, orientation="horizontal", height=25)

        self.le_file = oasysgui.lineEdit(file_box, self, "filename", label="Select file", addSpace=False, orientation="horizontal")

        gui.button(file_box, self, "...", callback=self.select_file)

        gui.separator(general_options_box)

        gui.button(general_options_box, self, "View/Refresh", callback=self.run_action, height=45)


        # MAIN AREA
        self.main_tabs = oasysgui.tabWidget(self.mainArea)

        plot_tab = oasysgui.createTabPage(self.main_tabs, "Plots")
        out_tab = oasysgui.createTabPage(self.main_tabs, "Output")



    def select_file(self):
        self.filename = oasysgui.selectFileFromDialog(self, self.filename, "Open File", file_extension_filter="*.*")
        self.le_file.setText(self.filename)

    def run_action(self):
        # if ConfirmDialog.confirmed(self):
        self.view(self.load_file_to_numpy_array())
        self.send("filename", self.filename)

    def set_input(self, input_data):
        self.filename = input_data

    def load_file_to_numpy_array(self):
        npimg = mpimg.imread(self.filename)
        return npimg

    def view(self,npimg,colorbar=True):
        cmap = None
        cmap = "hot"
        cmap = 'nipy_spectral'

        imgplot = plt.imshow(npimg, cmap=cmap)
        if colorbar:
            plt.colorbar()
        plt.show()

if __name__ == "__main__":

    import sys
    from oasys.widgets.exchange import DataExchangeObject

    app = QApplication(sys.argv)
    w = OWFileSelector()

    w.show()

    app.exec()
    w.saveSettings()
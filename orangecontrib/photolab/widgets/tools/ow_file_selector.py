from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

from orangewidget import gui
from orangewidget.settings import Setting

from oasys.widgets import widget
import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

from orangecontrib.photolab.widgets.gui.ow_photolab_widget import OWPhotolabWidget
from orangecontrib.photolab.util.photolab_objects import PLPhoto


# import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout


class OWFileSelector(OWPhotolabWidget):
    name = "File Selector"
    description = "File Selector"
    icon = "icons/selector.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "msanchezdelrio@gmail.com"
    priority = 10
    category = "Tools"
    keywords = ["data", "file", "load", "read"]


    outputs = [
                {"name": "PLPhoto",
                "type": PLPhoto,
                "doc": "photolab photo",
                "id": "photolab photo"},
                {"name": "filename",
                 "type": str,
                 "doc": "selected file name",
                 "id": "filename"},
               ]

    want_main_area=1


    filename = Setting("None")
    input_data = PLPhoto()

    def __init__(self):
        super().__init__()

        file_box = oasysgui.widgetBox(self.general_options_box, "", addSpace=False, orientation="vertical", height=25)
        self.le_file = oasysgui.lineEdit(file_box, self, "filename", label="Select file", addSpace=False, orientation="horizontal")


        file_box = oasysgui.widgetBox(self.general_options_box, "", addSpace=False,
                                      orientation="vertical")
        self.model = QFileSystemModel()
        self.model.setRootPath('/Users/srio/Desktop/')
        self.tree = QTreeView(file_box)
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(370, 600)
        self.tree.clicked.connect(self.onClicked)

        file_box = oasysgui.widgetBox(self.general_options_box, "", addSpace=False, orientation="vertical", height=25)


    def onClicked(self, index):
        path = self.sender().model().filePath(index)
        print(path)
        self.le_file.setText(path)
        self.process()

    def select_file(self):
        self.filename = oasysgui.selectFileFromDialog(self, self.filename, "Open File", file_extension_filter="*.*")
        self.le_file.setText(self.filename)

    def process_specific(self):

        self.input_data.set_url(self.filename)
        self.input_data.load()

        self.photolab_output.setText("\nCurrent image: \n" + self.input_data.info())

        self.preview(self.input_data.image())

        self.send("filename", self.filename)
        self.send("PLPhoto", self.input_data)

        self.photolab_python_script.set_code(self.input_data.to_python_code())


    def set_input(self, input_data):
        pass

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)
    w = OWFileSelector()

    w.filename = "/Users/srio/Public/ines/DSC_1575.jpg"

    w.show()

    app.exec()
    w.saveSettings()
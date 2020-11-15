import sys

from oasys.widgets import widget
from PyQt5 import QtWidgets

from orangewidget import gui
from orangewidget.settings import Setting

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QTextCursor

import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy

from orangecontrib.photolab.widgets.gui.python_script import PythonScript
from oasys.util.oasys_util import TriggerIn, EmittingStream

# import matplotlib.pyplot as plt
import matplotlib
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class OWPhotolabWidget(widget.OWWidget):

    want_main_area=1

    is_automatic_run = Setting(True)

    error_id = 0
    warning_id = 0
    info_id = 0


    IMAGE_WIDTH = 760
    IMAGE_HEIGHT = 545
    MAX_WIDTH = 1320
    MAX_HEIGHT = 700
    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560

    view_type = Setting(1)

    def __init__(self, show_general_option_box=True, show_automatic_box=False, show_view_options=True, show_script_tab=True):
        super().__init__()

        self.leftWidgetPart.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.leftWidgetPart.setMaximumWidth(self.CONTROL_AREA_WIDTH + 20)
        self.leftWidgetPart.updateGeometry()


        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        # CONTROL AREA
        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        gui.button(self.controlArea, self, "Process", callback=self.process, height=45)
        gui.separator(self.controlArea)


        self.general_options_box = gui.widgetBox(self.controlArea, "General Options", addSpace=True, orientation="vertical")
        self.general_options_box.setVisible(show_general_option_box)

        if show_automatic_box :
            gui.checkBox(self.general_options_box, self, 'is_automatic_run', 'Automatic Execution')


        # MAIN AREA
        self.main_tabs = oasysgui.tabWidget(self.mainArea)

        ##
        tab_preview = oasysgui.createTabPage(self.main_tabs, "Preview")


        ######################
        if show_view_options == True:
            view_box = oasysgui.widgetBox(tab_preview, "Results Options", addSpace=False, orientation="horizontal")
            view_box_1 = oasysgui.widgetBox(view_box, "", addSpace=False, orientation="vertical", width=350)

            self.view_type_combo = gui.comboBox(view_box_1, self, "view_type", label="View Results",
                                                labelWidth=220,
                                                items=["No", "Yes"],
                                                callback=self.set_ViewType, sendSelectedValue=False, orientation="horizontal")
        else:
            self.view_type = 1



        self.preview_id = gui.widgetBox(tab_preview, "", addSpace=True, orientation="vertical")

        ##
        tab_info = oasysgui.createTabPage(self.main_tabs, "Info")
        self.photolab_output = oasysgui.textArea() #height=self.IMAGE_HEIGHT-35)
        info_box = oasysgui.widgetBox(tab_info, "", addSpace=True, orientation="horizontal") #, height = self.IMAGE_HEIGHT-20, width = self.IMAGE_WIDTH-20)
        info_box.layout().addWidget(self.photolab_output)

        #
        # add script tab to tabs panel
        #
        if show_script_tab:
            script_tab = oasysgui.createTabPage(self.main_tabs, "Script")
            self.photolab_python_script = PythonScript()
            self.photolab_python_script.code_area.setFixedHeight(400)
            script_box = gui.widgetBox(script_tab, "Python script", addSpace=True, orientation="horizontal")
            script_box.layout().addWidget(self.photolab_python_script)


    def callResetSettings(self):
        if ConfirmDialog.confirmed(parent=self, message="Confirm Reset of the Fields?"):
            try:
                self.resetSettings()
            except:
                pass

    def process(self):
        self.photolab_output.setText("")
        self.progressBarInit()

        sys.stdout = EmittingStream(textWritten=self.writeStdOut)

        if self.input_data is None: raise Exception("No Input Data")

        self.process_specific()

        self.progressBarFinished()

    def preview(self, current_image):

        if self.view_type == 1:
            if current_image is None:
                raise Exception("Please load an image....")

            f = Figure()
            figure_canvas = FigureCanvasQTAgg(f)
            toolbar = NavigationToolbar(figure_canvas, self)
            ax = f.add_subplot(111)
            ax.imshow(current_image[:,:,:])
            ax.set_xticks([], minor=False)
            ax.set_yticks([], minor=False)


            try:
                self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(1))
                self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(0))
            except:
                pass
            self.preview_id.layout().addWidget(toolbar)
            self.preview_id.layout().addWidget(figure_canvas)


    def writeStdOut(self, text):
        cursor = self.photolab_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.photolab_output.setTextCursor(cursor)
        self.photolab_output.ensureCursorVisible()


    def set_ViewType(self):
        try:
            self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(1))
            self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(0))

        except:
            pass
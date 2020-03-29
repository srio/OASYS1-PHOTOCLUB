
from oasys.widgets import widget

from orangewidget import gui
from orangewidget.settings import Setting

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect

import oasys.widgets.gui as oasysgui
from oasys.widgets.gui import ConfirmDialog

from PyQt5.QtWidgets import QApplication, QMessageBox, QSizePolicy

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

    # MAX_WIDTH = 1320
    # MAX_HEIGHT = 700
    # CONTROL_AREA_WIDTH = 405
    # TABS_AREA_HEIGHT = 560

    IMAGE_WIDTH = 760
    IMAGE_HEIGHT = 545
    MAX_WIDTH = 1320
    MAX_HEIGHT = 700
    CONTROL_AREA_WIDTH = 405
    TABS_AREA_HEIGHT = 560

    # photolab_live_propagation_mode = "Unknown"

    def __init__(self, show_general_option_box=True, show_automatic_box=False):
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
        self.preview_id = gui.widgetBox(tab_preview, "", addSpace=True, orientation="vertical")
        # self.preview_id.setFixedHeight(self.TABS_AREA_HEIGHT - 30)
        # self.preview_id.setFixedWidth(self.TABS_AREA_WIDTH - 20)

        ##
        tab_info = oasysgui.createTabPage(self.main_tabs, "Info")
        self.info_id = oasysgui.textArea() #height=self.IMAGE_HEIGHT-35)
        info_box = oasysgui.widgetBox(tab_info, "", addSpace=True, orientation="horizontal") #, height = self.IMAGE_HEIGHT-20, width = self.IMAGE_WIDTH-20)
        info_box.layout().addWidget(self.info_id)

        ##
        tab_script = oasysgui.createTabPage(self.main_tabs, "Script")

        ## data
        self.current_image = None

    def callResetSettings(self):
        if ConfirmDialog.confirmed(parent=self, message="Confirm Reset of the Fields?"):
            try:
                self.resetSettings()
            except:
                pass

    def process(self):
        raise Exception("To be defined in the subclass")

    def preview(self):
        if self.current_image is None:
            raise Exception("Please load an image....")

        f = Figure()
        figure_canvas = FigureCanvasQTAgg(f)
        toolbar = NavigationToolbar(figure_canvas, self)
        ax = f.add_subplot(111)
        ax.imshow(self.current_image[:,:,:])

        ax.set_xticks([], minor=False)
        ax.set_yticks([], minor=False)

        self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(1))
        self.preview_id.layout().removeItem(self.preview_id.layout().itemAt(0))
        self.preview_id.layout().addWidget(toolbar)
        self.preview_id.layout().addWidget(figure_canvas)
        
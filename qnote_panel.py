# -*- coding: utf-8 -*-

from qgis.PyQt.QtWidgets import QDockWidget, QAction
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt import uic
from os import path


pluginPath = path.dirname(path.abspath(__file__))
FORM_CLASS, _ = uic.loadUiType(path.join(pluginPath, 'ui_qnote.ui'))

class MainPanel(QDockWidget, FORM_CLASS):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.add_hyperlink = QAction(QIcon(path.join(pluginPath, "link_image.jpg")), "Add hyperlink")
        self.add_hyperlink.triggered.connect(self.addHyperlink)
        self.toolbar.addAction( self.add_hyperlink )
    
    def addHyperlink(self):
        self.edit.showAddHyperLinkUi(self.edit.textCursor())
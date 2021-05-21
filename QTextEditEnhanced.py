import sys
from PyQt5.QtWidgets import QTextEdit, QMenu, QDialog
from PyQt5.Qt import QDesktopServices, QUrl, QApplication, Qt, QBrush, QTextCharFormat
from qgis.PyQt import uic
from os import path


class QTextEditEnhanced(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if self.anchorAt(e.pos()):
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        super()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            menu = QMenu(self)
            addHyperLinkAction = menu.addAction("Add Hyperlink")
            action = menu.exec_(self.mapToGlobal(e.pos()))
            if action == addHyperLinkAction:
                cursor = self.cursorForPosition(e.pos())
                self.showAddHyperLinkUi(cursor)
        super()

    def mouseReleaseEvent(self, e):
        url = QUrl.fromLocalFile(self.anchorAt(e.pos()))
        QDesktopServices.openUrl(url)
        super()

    def showAddHyperLinkUi(self, cursor):
        pluginPath = path.dirname(path.abspath(__file__))
        window = uic.loadUi(
            path.join(pluginPath, "ui_hyperlink.ui"))
        if window.exec_() == QDialog.Accepted:
            linkName = window.textInput_displayText.text()
            linkAddress = window.textInput_url.text()
            cursor.insertHtml(
                '<a href="%s">%s</a>' % (linkAddress, linkName))
            charFormat = QTextCharFormat()
            charFormat.setForeground(QBrush())
            cursor.insertText(" ", charFormat)

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qNote
                                 A QGIS plugin
 Save notes in QGIS projects
                              -------------------
        begin                : 2012-03-31
        copyright            : (C) 2012 by Piotr Pociask
        email                : opengis84 (at) gmail (dot) com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
import os
# Import the code for the dialog
#from qnotedialog import qNoteDialog

class qNote:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # Create the dialog and keep reference
        #self.dlg = qNoteDialog()
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/qnote"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/qnote_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)        
    
    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/qnote/icon.png"), u"qNote", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        

        proj = QgsProject.instance()
        QObject.connect(proj, SIGNAL("readProject(const QDomDocument &)"),self.loadData)
        QObject.connect(proj, SIGNAL("writeProject(QDomDocument &)"),self.saveData)
        QObject.connect(self.iface, SIGNAL("newProjectCreated ()"),self.clearEdit)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&qNote", self.action)
        
        path = os.path.dirname(os.path.abspath(__file__))
        self.dock = uic.loadUi(os.path.join(path, "ui_qnote.ui"))
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&qNote",self.action)
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeDockWidget(self.dock)

    # run method that performs all the real work
    def run(self):
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.loadData()
        """
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass"""
            
    def saveData(self):
        proj = QgsProject.instance()
        text = self.dock.edit.toPlainText()
        if text:
            proj.writeEntry('qnote', 'text', text)
        else:
            proj.removeEntry('qnote', 'text')

    
    def loadData(self):
        proj = QgsProject.instance()
        text = proj.readEntry('qnote', 'text', '')[0]
        self.dock.edit.setText( text )
    
    def clearEdit(self):
        self.dock.edit.setText('')
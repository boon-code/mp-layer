#!/usr/bin/env python

import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSignal, QString, QModelIndex)
from PyQt4.QtGui import (QItemSelection, QMainWindow, QApplication,
                         QItemSelectionModel)
from PyQt4 import QtGui
from gui import Ui_MPLayerGui
import naming
import download


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


DL_PATH = ""


class EpisodeController(QObject):
    
    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)
    
    def __init__(self, controller):
        QObject.__init__(self)
        self._ctrl = controller
        self._nameStorage = controller.nameStorage
        self._dlList = controller.dlList
        self._ui = controller.ui
        self._selModel = self._ui.lvSeries.selectionModel()
        self._ui.pubAddEpisode.setEnabled(False)
    
    def doConnections(self):
        ui = self._ui
        ui.ledEName.textChanged.connect(self.changedEpisodeName)
        ui.spnEpisode.valueChanged.connect(self.checkEpisode)
        ui.spnSeason.valueChanged.connect(self.checkEpisode)
        self._ctrl.changedURL.connect(self._updateEpisode)
        ui.pubAddEpisode.clicked.connect(self.addEpisode)
        model = self._selModel
        model.currentChanged.connect(self.selectedEpisodeChanged)
    
    @pyqtSlot(QModelIndex, QModelIndex)
    def selectedEpisodeChanged(self, sel, desl):
        series = self._nameStorage.get(sel)
        if series is not None:
            self._ui.ledEName.setText(series.name)
    
    @pyqtSlot(QString)
    def changedEpisodeName(self, text):
        self._updateEpisode()
        ret, index = self._nameStorage.find(text)
        if ret:
            self._selModel.setCurrentIndex(index,
                            QItemSelectionModel.SelectCurrent)
        else:
            self._selModel.clear()
    
    @pyqtSlot()
    def addEpisode(self):
        series = self._nameStorage.get(self._selModel.currentIndex())
        if series is not None:
            ui = self._ui
            season = ui.spnSeason.value()
            episode = ui.spnEpisode.value()
            if not series.inProgress(season, episode):
                inst = series.createInstance(ui.pteUrl.toPlainText(),
                                             season, episode)
            inst.finished.connect(self.checkEpisode)
            self.checkEpisode()
    
    @pyqtSlot()
    def checkEpisode(self):
        ui = self._ui
        text = ""
        if not ui.ledEName.text().isEmpty():
            series = self._nameStorage.get(self._selModel.currentIndex())
            if series is not None:
                season = ui.spnSeason.value()
                episode = ui.spnEpisode.value()
                if series.inProgress(season, episode):
                    text = "This Episode is just downloading"
                elif series.inHistory(ui.spnSeason.value(),
                                    ui.spnEpisode.value()):
                    text = "Has already been downloaded once!"
        ui.labEInstance.setText(text)
    
    @pyqtSlot()
    def _updateEpisode(self):
        ui = self._ui
        enabled = True
        if ui.ledEName.text().isEmpty():
            enabled = False
        elif ui.pteUrl.toPlainText().isEmpty():
            enabled = False
        ui.pubAddEpisode.setEnabled(enabled)


class Controller(QObject):
    
    changedURL = pyqtSignal()
    
    def __init__(self, dl_path=DL_PATH):
        QObject.__init__(self)
        self._gui = QMainWindow()
        self.ui = Ui_MPLayerGui()
        self.ui.setupUi(self._gui)
        self.dlList = download.DownloadList(dl_path)
        self.nameStorage = naming.SeriesStorage()
        self.valid_url = False
        self.ui.pubAddSimple.setEnabled(False)
        self.ui.lvSeries.setModel(self.nameStorage)
        self._epiController = EpisodeController(self)
        self._doConnections()
    
    @pyqtSlot()
    def _changedURL(self):
        """URL has been changed.
        
        This slot checks if the url widget is empty, and 
        sends out a signal if the empty status changed since
        the last message.
        """
        url_empty = self.ui.pteUrl.toPlainText().isEmpty()
        if url_empty and self.valid_url:
            self.valid_url = False
            self.changedURL.emit()
        elif (not url_empty) and (not self.valid_url):
            self.valid_url = True
            self.changedURL.emit()
    
    @pyqtSlot()
    def _updateSimpleButton(self):
        """This slot checks if simple download button should be enabled.
        
        This slot reads the valid_url member and checks the current
        status (empty?) of the LineEdit ledMName.
        """
        enabled = False
        if self.valid_url and not self.ui.ledMName.text().isEmpty():
            enabled = True
        if self.ui.pubAddSimple.isEnabled != enabled:
            self.ui.pubAddSimple.setEnabled(enabled)
    
    def _doConnections(self):
        self.ui.pteUrl.textChanged.connect(self._changedURL)
        self.ui.ledMName.textChanged.connect(self._updateSimpleButton)
        self._epiController.doConnections()
        self.changedURL.connect(self._updateSimpleButton)
    
    def show(self):
        self._gui.show()
    
    def convertName(self, name, is_episode=False):
        pass
    
    @pyqtSlot(QString)
    def changedEpisodeName(self, text):
        
        print "changed:", text
    
    @pyqtSlot()
    def addSimple(self):
        pass


def main():
    app = QApplication(sys.argv)
    QtGui.qApp = app
    c = Controller()
    c.show()
    ret = app.exec_()
    del c
    del app
    sys.exit(ret)
    


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSignal, QString)
from PyQt4.QtGui import (QItemSelection, QMainWindow, QApplication)
from PyQt4 import QtGui
from gui import Ui_MPLayerGui
import naming
import download

DL_PATH = ""


class EpisodeController(QObject):
    
    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)
    
    def __init__(self, ui):
        QObject.__init__(self)
        # ui elements:
        #ui.ledEName
        #ui.ledTitle
        #ui.spnSeason
        #ui.spnEpisode
        #ui.pubAddEpisode
        #ui.lvSeries
        #ui.pteUrl
        # member:
        self._ui = ui
    
    def doConnections(self):
        ui = self._ui
        QObject.connect(ui.ledEName, SIGNAL("textChanged(QString)"),
                        self.changedEpisodeName)
        QObject.connect(ui.spnEpisode, SIGNAL("valueChanged(int)"),
                        self.changedEpisodeNr)
        QObject.connect(ui.spnSeason, SIGNAL("valueChanged(int)"),
                        self.changedSeasonNr)
        QObject.connect(ui.pubAddEpisode, SIGNAL("clicked()"),
                        self.addEpisode)
        
    @pyqtSlot(QString)
    def changedEpisodeName(self, text):
        self.update()
    
    @pyqtSlot(int)
    def changedEpisodeNr(self, number):
        pass
    
    @pyqtSlot(int)
    def changedSeasonNr(self, number):
        pass
    
    @pyqtSlot()
    def addEpisode(self):
        pass
    
    def update(self):
        ui = self._ui
        enabled = True
        if ui.ledEName.text().isEmpty():
            enabled = False
        ui.pubAddEpisode.addEpisode.setEnabled(enabled)

class Controller(QObject):
    
    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)
    
    def __init__(self, dl_path=DL_PATH):
        QObject.__init__(self)
        self._gui = QMainWindow()
        self._ui = Ui_MPLayerGui()
        self._ui.setupUi(self._gui)
        self._dlList = download.DownloadList(dl_path)
        self._nameStorage = naming.SeriesStorage()
        self._epiController = EpisodeController(self._ui)
        self._doConnections()
    
    def _doConnections(self):
        self._epiController.doConnections()
    
    def show(self):
        self._gui.show()
    
    def convertName(self, name, is_episode=False):
        pass
    
    @pyqtSlot(QString)
    def changedEpisodeName(self, text):
        
        print "changed:", text
    
    @pyqtSlot()
    def addEpisode(self):
        uiName = self._ui.ledEName
        series = self._nameStorage.getOrCreateSeries(uiName.text())
        print series.name
    
    @pyqtSlot()
    def addSimple(self):
        pass
    
    @pyqtSlot(QItemSelection, QItemSelection)
    def selectedDownloadChanged(self, selected, deselected):
        pass
    
    @pyqtSlot(QItemSelection, QItemSelection)
    def selectedSeriesChanged(self, selected, deselected):
        pass
    
    @pyqtSlot(int)
    def userChangedEpisode(self, number):
        pass
    
    @pyqtSlot(int)
    def userChangedSeason(self, number):
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

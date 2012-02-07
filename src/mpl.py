#!/usr/bin/env python

import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSignal, QString)
from PyQt4.QtGui import (QItemSelection, QMainWindow, QApplication,
                         QItemSelectionModel)
from PyQt4 import QtGui
from gui import Ui_MPLayerGui
import naming
import download

DL_PATH = ""


class EpisodeController(QObject):
    
    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)
    
    def __init__(self, ui, dl_list, name_storage):
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
        self._nameStorage = name_storage
        self._dlList = dl_list
        self._ui = ui
        ui.lvSeries.setModel(self._nameStorage)
        self._selModel = ui.lvSeries.selectionModel()
        ui.pubAddEpisode.setEnabled(False)
    
    def doConnections(self):
        ui = self._ui
        QObject.connect(ui.ledEName, SIGNAL("textChanged(QString)"),
                        self.changedEpisodeName)
        QObject.connect(ui.pteUrl, SIGNAL("textChanged()"),
                        self.changedURL)
        QObject.connect(ui.spnEpisode, SIGNAL("valueChanged(int)"),
                        self.changedEpisodeNr)
        QObject.connect(ui.spnSeason, SIGNAL("valueChanged(int)"),
                        self.changedSeasonNr)
        QObject.connect(ui.pubAddEpisode, SIGNAL("clicked()"),
                        self.addEpisode)
        QObject.connect(self._selModel,
                        SIGNAL("currentChanged(QModelIndex, QModelIndex)"),
                        self.selectedEpisodeChanged)
        #QObject.connect(ui.
    
    @pyqtSlot()
    def changedURL(self):
        self._update()
    
    @pyqtSlot()
    def selectedEpisodeChanged(self, sel, desl):
        
        print "currentChanged:"
        print "  sel ", sel.isValid()
        if sel.isValid():
            print "  - ", sel.row()
        print "  desl ", desl.isValid()
        if desl.isValid():
            print "  - ", desl.row()
        
        text = self._nameStorage.get(sel)
        if text is not None:
            self._ui.ledEName.setText(text.name)
    
    @pyqtSlot(QString)
    def changedEpisodeName(self, text):
        self._update()
        ret, index = self._nameStorage.find(text)
        if ret:
            print "select index", index.row()
            self._selModel.setCurrentIndex(index,
                                           QItemSelectionModel.SelectCurrent)
        else:
            self._selModel.clear()
    
    @pyqtSlot(int)
    def changedEpisodeNr(self, number):
        pass
    
    @pyqtSlot(int)
    def changedSeasonNr(self, number):
        pass
    
    @pyqtSlot()
    def addEpisode(self):
        pass
    
    def _checkSeries(self):
        pass
    
    def _update(self):
        ui = self._ui
        enabled = True
        print "update"
        if ui.ledEName.text().isEmpty():
            enabled = False
        elif ui.pteUrl.toPlainText().isEmpty():
            enabled = False
        ui.pubAddEpisode.setEnabled(enabled)


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
        self._epiController = EpisodeController(self._ui, self._dlList,
                                                self._nameStorage)
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

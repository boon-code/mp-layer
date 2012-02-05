#!/usr/bin/env python

import sys
import logging

from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSlot)
from PyQt4.QtGui import QItemSelection
import naming
import download


_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"


class Controller(QObject):
    
    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)
    
    def __init__(self):
        QObject.__init__(self)
    
    def convertName(self, name, isEpisode=False):
        pass
    
    @pyqtSlot(str)
    def changedEpisodeName(self, text):
        pass
    
    @pyqtSlot()
    def addEpisode(self):
        pass
    
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
    pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python


import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from os.path import split, normpath, join, exists

class TestStreamer(QObject):
    
    RUN_BIT = 1
    FIN_BIT = 2
    ERROR_BIT = 4
    
    _READY = 0
    _RUNNING = RUN_BIT
    _FINISHED_SUC = FIN_BIT
    _FINISHED_ERR = ERROR_BIT | FIN_BIT
    
    _current_id = 0
    
    changedStatus = pyqtSignal(int)
    
    def __init__(self, dlinfo, mp_path="mplayer", name="worker"):
        """Creates and initializes a new streamer object.
        
        :param dlinfo:  Download info container
        :param mp_path: Optional path to the mplayer (used to download
                        the stream).
        :param name:    Optional name of this streamer (This name
                        will be used in debug messages...).
        """
        QObject.__init__(self)
        self._info = dlinfo
        self._mplayer = mp_path
        self._name = "%s_01" % name
        self._status = self._READY
        self._lerror = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._next)
        self._size = 0
    
    def __str__(self):
        return self._info.getFilename()
    
    def start(self, overwrite=False):
        self._status = self._RUNNING
        self.changedStatus.emit(self._status)
        self._timer.start(400)
        self._size = 0
    
    @pyqtSlot()
    def _next(self):
        if self._size > 50:
            self._status = self.FIN_BIT
            self.changedStatus.emit(self._status)
            self._info.finished.emit(True)
            self._timer.stop()
        else:
            self._size += 1
    
    def getSize(self, inc_unit=False):
        if self._size > 0:
            return u"%dM" % self._size
    
    def kill(self):
        if self._status & self.RUN_BIT:
            self._status = self._FINISHED_ERR
            self._timer.stop()
            self.changedStatus.emit(self._status)
    
    def discard(self):
        self._info.removed.emit()
    
    def getStatus(self):
        return self._status

STORAGE_FILE = "mpl-storage.json"

def testInteractive():
    import mpl
    import download as d
    import PyQt4.QtCore as core
    import PyQt4.QtGui as gui
    app = gui.QApplication(sys.argv)
    path = sys.argv[1]
    storepath = join(path, STORAGE_FILE)
    gui.qApp = app
    c = mpl.Controller(store_file=storepath)
    c.setDLPath(path)
    c.show()
    n = c.nameStorage
    dl = c.dlList
    inf = d.DownloadInfo("url", "bla", "path")
    streamer = TestStreamer(inf)
    streamer.changedStatus.connect(dl._streamerStatusChanged)
    dl._dllist.append(streamer)
    idx = dl._dllist.index(streamer)
    dl._idbypath[inf.getFilename()] = idx
    dl.reset()
    ret = app.exec_()
    del n
    del c
    del dl
    del app
    sys.exit(ret)


def main():
    testInteractive()


if __name__ == '__main__':
    base = split(sys.argv[0])[0]
    path = normpath(join(base, "../src/"))
    sys.path.insert(0, path)
    main()

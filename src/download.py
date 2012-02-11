import logging
import os
from subprocess import Popen
from os.path import join, isdir, exists
from PyQt4.QtCore import (QObject, pyqtSignal, QAbstractListModel, Qt,
                          QVariant, pyqtSlot, QProcess)


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


_log = logging.getLogger(__name__)
_DEFAULT_PATH = os.getcwd()


class DownloadException(Exception):
    pass


class FileExistsError(DownloadException):
    
    def __init__(self, path):
        self.path = path


class AlreadyRunningError(DownloadException):
    
    def __init__(self, filepath):
        self.file = filepath


class InvalidPathError(DownloadException):
    
    def __init__(self, path):
        self.path = path


class DownloadInfo(QObject):
    
    finished = pyqtSignal('bool')
    
    def __init__(self, url, filename):
        QObject.__init__(self)
        self._url = url
        self._filename = filename
    
    def getSourceURL(self):
        return self._url
    
    def getFilename(self):
        return self._filename


class DownloadList(QAbstractListModel):
    
    invalidDLPath = pyqtSignal()
    
    def __init__(self, dl_path=_DEFAULT_PATH, autostart=True):
        self._dlpath = dl_path
        self._autostart = autostart
        self._dllist = list()
        self._idbypath = dict()
    
    @pyqtSlot('bool')
    def setAutostart(self, autostart):
        self._autostart = autostart
    
    @pyqtSlot(QString)
    def setDLPath(self, path):
        path = str(path)
        if isdir(path):
            self._dlpath = path
    
    def _addDownload(self, path):
        self._dllist = MPStreamer
    
    def add(self, dlinfo):
        path = join(self._dlpath, dlinfo.getFilename())
        # TODO: continue
    
    def remove(self, index):
        pass
    
    def kill(self, index):
        pass
    
    def getStreamer(self, index):
        pass


class MPStreamer(QObject):
    
    RUN_BIT = 1
    FIN_BIT = 2
    ERROR_BIT = 2
    
    _READY = 0
    _RUNNING = RUN_BIT
    _FINISHED_SUC = FIN_BIT
    _FINISHED_ERR = ERROR_BIT | FIN_BIT
    
    _current_id = 0
    
    finished = pyqtSignal(bool)
    changedStatus = pyqtSignal(int)
    
    @classmethod
    def nextId(cls):
        """Generates unique id's.
        
        This class method is used to generate unique id's
        for all MPStreamer instances. (Not thread safe)
        """
        cid = cls._current_id
        cls._current_id += 1
        return cid
    
    def __init__(self, url, path, mp_path="mplayer", name="worker"):
        self._url = url
        self._path = path
        self._mplayer = mp_path
        self._name = "%s_%02d" % (name, self.nextId())
        self._proc = QProcess()
        self._status = self._READY
        self._doConnections()
    
    def _doConnection(self):
        self._proc.finished.connect(self._qprocessFinished)
        self._proc.stateChanged.connect(self.qprocessStateChanged)
    
    def start(self, overwrite=False):
        if self._status & self.RUN_BIT:
            raise AlreadyRunningError(self._path)
        elif exists(self._path) and (not overwrite):
            raise FileExistsError(self._path)
        else:
            if self._status & self.FIN_BIT:
                _log.debug("Restarting Download of file '%s'"
                           % self._path)
            args = ["-dumpstream", "-dumpfile", self._path, self._url]
            self._proc.start(self._mplayer, args)
    
    def _qprocessStateChanged(self, new_state):
        old_status = self._status
        if new_state != self.NotRunning:
            self._status = self._RUNNING
        else:
            self._status &= ~(self.RUN_BIT)
        if old_status != self._status:
            self.changedStatus.emit(self._status)
    
    def _qprocessFinished(self, exit_code, exit_status):
        old_status = self._status
        self._status |= self.FIN_BIT
        if exit_status == QProcess.NormalExit:
            # further checking...
            self._status |= self.SUCCESS_BIT
        else:
            self._status |= self.ERROR_BIT
        
        if self._status != old_status:
            self.changedStatus.emit(self._status)
    
    def kill(self):
        self._proc.kill()
    
    def getStatus(self):
        return self._status


if __name__ == '__main__':
    pass

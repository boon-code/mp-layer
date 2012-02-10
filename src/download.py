import logging
import os
from subprocess import Popen
from os.path import join, isdir
from PyQt4.QtCore import (QObject, pyqtSignal, QAbstractListModel, Qt,
                          QVariant, pyqtSlot)


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


class AlreadyStartedError(DownloadException):
    
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
    
    def remove(self, index):
        pass
    
    def kill(self, index):
        pass
    
    def getStreamer(self, index):
        pass


class MPStreamer(object):
    
    _id_lock = RLock()
    _current_id = 0
    
    @classmethod
    def nextId(cls):
        """Generates unique id's.
        
        This class method is used to generate unique id's
        for all MPStreamer instances. (Not thread safe)
        """
        cls._id_lock += 1
        return cls._id_lock
    
    def __init__(self, url, dl_path, mp_path="mplayer", name="worker"):
        self._url = url
        self._path = dl_path
        self._mplayer = mp_path
        self._name = "%s_%02d" % (name, self.nextId())
        self._proc = None
    
    def start(self, overwrite=False):
        if self._proc is not None:
            raise AlreadyStartedError(self._path)
        else:
            # TODO: Continue here!
            self._proc = subprocess.Popen(
    
    def _download(self):
        while True:
            cmd, fname, url = self._queue.get(True)
            if cmd == DOWNLOAD:
                pass
            elif cmd == EXIT:
                _log.debug(self.DBG_EXIT_CMD)
                return
            else:
                _log.info(self.INF_UNKNOWN_CMD % str(cmd[0]))
    
    def _dl_mplayer(self, fname, url):
        path = join(self._dl_path, fname)
        args = [self._mplayer, '-dumpstream', '-dumpfile', path,
          '"%s"' % url]
        process = Popen(args, stdout=PIPE, stderr=STDOUT)
        


if __name__ == '__main__':
    streamer1 = MPStreamer("../dl")

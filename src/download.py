import logging
from Queue import Queue
from threading import Thread, RLock
from subprocess import Popen, PIPE, STDOUT
from os.path import join
from PyQt4.QtCore import (QObject, pyqtSignal, QAbstractListModel, Qt,
                          QVariant)


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2011 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


_log = logging.getLogger(__name__)


DOWNLOAD = 1
EXIT = 2


class DownloadInfo(QObject):
    
    succeeded = pyqtSignal()
    
    def __init__(self, url, filename):
        QObject.__init__(self)
        self._url = url
        self._filename = filename
    
    def getSourceURL(self):
        return self._url
    
    def getFilename(self):
        return self._filename


class DownloadList(QAbstractListModel):
    
    def __init__(self, dl_path, autostart=True):
        self._dlpath = dl_path
        self._autostart = autostart
        self._dllist = list()
    
    def add(self, dlinfo):
        path = join(self._dlpath, dlinfo.getFilename())
    
    def remove(self, index):
        pass
    
    def kill(self, index):
        pass
    
    def getStreamer(self, index):
        pass


class MPStreamer(object):
    
    INF_UNKNOWN_CMD = "Ignoring unknown command received: '%s'"
    DBG_EXIT_CMD = "Received command exit!"
    
    _id_lock = RLock()
    _current_id = 0
    
    @classmethod
    def nextId(cls):
        _id_lock.acquire()
        try:
            id = _id_lock
            _id_lock += 1
            return id
        finally:
            _id_lock.release()
    
    def __init__(self, dl_path, mp_path="mplayer", name="worker"):
        self._dl = dl_path
        self._mplayer = mp_path
        self._queue = Queue()
        self._name = "%s_%02d" % (name, self.nextId())
        self._thread = Thread(target=self._workerloop)
    
    def _workerloop(self):
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

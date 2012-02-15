import logging
import os
import filetype
from subprocess import Popen
from os.path import join, isdir, exists, split
from os import rename
from PyQt4.QtCore import (QObject, pyqtSignal, QAbstractListModel, Qt,
                          QVariant, pyqtSlot, QProcess, QModelIndex)


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


class AlreadyAddedError(DownloadException):
    
    def __init__(self, filename):
        self.file = filename


class InvalidPathError(DownloadException):
    
    def __init__(self, path):
        self.path = path


class DownloadInfo(QObject):
    
    finished = pyqtSignal('bool')
    
    def __init__(self, url, filename, dest_dir='.'):
        QObject.__init__(self)
        self.dest_dir = dest_dir
        self._url = url
        self._filename = filename
    
    def getSourceURL(self):
        return self._url
    
    def getFilename(self):
        return self._filename
    
    def getPath(self):
        return join(self.dest_dir, self._filename)


class DownloadList(QAbstractListModel):
    
    invalidDLPath = pyqtSignal()
    
    def __init__(self, dl_path=_DEFAULT_PATH, autostart=True):
        QAbstractListModel.__init__(self, None)
        self._dlpath = dl_path
        self._autostart = autostart
        self._dllist = list()
        self._idbypath = dict()
    
    @pyqtSlot('bool')
    def setAutostart(self, autostart):
        self._autostart = autostart
    
    @pyqtSlot('QString')
    def setDLPath(self, path):
        path = str(path)
        if isdir(path):
            self._dlpath = path
    
    def add(self, dlinfo):
        dlinfo.dest_dir = self._dlpath
        name = dlinfo.getFilename()
        if name in self._idbypath:
            raise AlreadyAddedError(name)
        else:
            streamer = MPStreamer(dlinfo)
            self._dllist.append(streamer)
            self._idbypath[name] = self._dllist.index(streamer)
            self.reset()
    
    def remove(self, index):
        streamer = self.getStreamer(index)
        if streamer is not None:
            if streamer.getStatus() & streamer.RUN_BIT == 0:
                idx = self._idbypath.pop(str(streamer))
                self._dllist.pop(idx)
    
    def kill(self, index):
        streamer = self.getStreamer(index)
        if streamer is not None:
            if streamer.getStatus() & streamer.RUN_BIT != 0:
                streamer.kill()
    
    def getStreamer(self, index):
        if index.isValid():
            return self._dllist[index.row()]
    
    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(str(self._dllist[index.row()]))
        else:
            return QVariant()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._dllist)


class MPStreamer(QObject):
    
    RUN_BIT = 1
    FIN_BIT = 2
    ERROR_BIT = 4
    
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
        :param cls: The 'class' object that called this method.
        """
        cid = cls._current_id
        cls._current_id += 1
        return cid
    
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
        self._name = "%s_%02d" % (name, self.nextId())
        self._proc = QProcess()
        self._status = self._READY
        self._lerror = None
        self._doConnections()
    
    def __str__(self):
        return self._info.getFilename()
    
    def _doConnections(self):
        self._proc.finished.connect(self._qprocessFinished)
        self._proc.stateChanged.connect(self._qprocessStateChanged)
    
    def start(self, overwrite=False):
        # TODO: check if path exists and is accessible
        self._lerror = None
        if self._status & self.RUN_BIT:
            raise AlreadyRunningError(self._info.getPath())
        elif exists(self._path) and (not overwrite):
            raise FileExistsError(self._info.getPath())
        else:
            if self._status & self.FIN_BIT:
                _log.debug("Restarting Download of file '%s'"
                           % self._info.getPath())
            args = ["-nolirc", "-dumpstream", "-dumpfile",
                    self._info.getPath(), self._info.getSourceURL()]
            self._proc.start(self._mplayer, args)
    
    def _qprocessStateChanged(self, new_state):
        old_status = self._status
        _log.info("QProcess::stateChanged '%s'" % str(new_state))
        if new_state != QProcess.NotRunning:
            self._status = self._RUNNING
        else:
            self._status &= ~(self.RUN_BIT)
        if old_status != self._status:
            self.changedStatus.emit(self._status)
    
    def _receivedProcessErrorMsg(self):
        # BAD: I should find some better way to check...
        if self._lerror.find("Failed to open"):
            return True
        else:
            return False
    
    def _qprocessFinished(self, exit_code, exit_status):
        _log.info("QProcess::finished code='%s', status='%s'"
                  % (str(exit_code), str(exit_status)))
        _log.debug("stdout: '%s'" % str(self._proc.readAllStandardOutput()))
        self._lerror = str(self._proc.readAllStandardError())
        _log.debug("stderr: '%s'" % self._lerror)
        succeeded = False
        old_status = self._status
        self._status |= self.FIN_BIT
        if exit_status != QProcess.NormalExit:
            _log.debug("Process most likly crashed!")
            self._status |= self.ERROR_BIT
        elif exit_code != 0:
            # This doesn't really indicate an error... :(
            _log.debug("mplayer failed (exit-code: %d)!" % exit_code)
            self._status |= self.ERROR_BIT
        elif self._receivedProcessErrorMsg():
            _log.debug("mplayer couldn't open url")
            self._status |= self.ERROR_BIT
        else:
            path = self._info.getPath()
            try:
                ext = filetype.ExtGuesser(path).get()
            except filetype.InvalidPathError as ex:
                _log.critical("Downloaded file '%s' seems to not exist."
                              % ex.path)
                self._status = self._FINISHED_ERR
            except filetype.ExternalProgramError:
                _log.critical("External program to guess ext. failed!")
                self._status = self._FINISHED_ERR
            else:
                _log.debug("Renaming '%s' to '%s'."
                           % (path, path + "." + ext))
                rename(path, path + "." + ext)
                succeeded = True
        if self._status != old_status:
            self.changedStatus.emit(self._status)
        self.finished.emit(succeeded)
    
    def kill(self):
        self._proc.kill()
    
    def getStatus(self):
        return self._status


if __name__ == '__main__':
    pass

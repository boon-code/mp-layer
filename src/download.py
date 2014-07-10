import logging
import os
import filetype
from subprocess import Popen
from os.path import join, isdir, exists, split, getsize, splitext
from PyQt4.QtCore import (QObject, pyqtSignal, QAbstractListModel, Qt,
                          QVariant, pyqtSlot, QProcess, QModelIndex)
from PyQt4.QtGui import QColor, QBrush, QPixmap, QIcon


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__docformat__ = "restructuredtext en"


_log = logging.getLogger(__name__)

_SIZE_MAX = (1024**4, 1024**3, 1024**2, 1024**1, 1)
_SIZE_PREFIX = ('TB', 'GB', 'MB', 'KB', 'B')


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

    finished = pyqtSignal(bool)
    removed = pyqtSignal()

    def __init__(self, url, filename, dest_dir='.'):
        QObject.__init__(self)
        self.destDir = dest_dir
        self._url = url
        self._filename = filename
        self._ext = None

    def getSourceURL(self):
        return self._url

    def getFilename(self):
        return self._filename

    def setExtension(self, ext=None):
        self._ext = ext

    def getPath(self):
        if self._ext is None:
            filename = self._filename
        else:
            filename = "%s.%s" % (self._filename, self._ext)
        return join(self.destDir, filename)


class DownloadList(QAbstractListModel):

    invalidDLPath = pyqtSignal()
    safeToExit = pyqtSignal(bool)

    def __init__(self, mplayerpgm='mplayer'):
        QAbstractListModel.__init__(self, None)
        self._mplayer_path = mplayerpgm
        self._dllist = list()
        self._idbypath = dict()
        pix = QPixmap(22, 22)
        pix.fill(QColor(0, 0, 255, 255))
        self._icon_run = QIcon(pix)
        pix = QPixmap(22, 22)
        pix.fill(QColor(255, 0, 0, 255))
        self._icon_error = QIcon(pix)
        pix = QPixmap(22, 22)
        pix.fill(QColor(0, 255, 0, 255))
        self._icon_fin = QIcon(pix)
        pix = QPixmap(22, 22)
        pix.fill(QColor(0, 0, 0, 255))
        self._icon_wait = QIcon(pix)

    def add(self, dlinfo):
        name = dlinfo.getFilename()
        if name in self._idbypath:
            raise AlreadyAddedError(name)
        else:
            streamer = MPStreamer(dlinfo)
            self._dllist.append(streamer)
            idx = self._dllist.index(streamer)
            self._idbypath[name] = idx
            streamer.changedStatus.connect(self._streamerStatusChanged)
            model_index = self.createIndex(idx, 0)
            self.dataChanged.emit(model_index, model_index)
            # This should be a better way to archive an update...
            # self.reset()
            return model_index

    def start(self, index, overwrite=False, wget=None):
        streamer = self.getStreamer(index)
        if streamer is not None:
            streamer.start(overwrite=overwrite, wget=wget)

    def remove(self, index):
        streamer = self.getStreamer(index)
        if streamer is not None:
            if streamer.getStatus() & streamer.RUN_BIT == 0:
                idx = self._idbypath.pop(str(streamer))
                self._dllist.pop(idx)
                self.reset()
                streamer.discard()
                self._streamerStatusChanged(0)
                # TRICKY: force check if we could close the window...

    def kill(self, index):
        streamer = self.getStreamer(index)
        if streamer is not None:
            if streamer.getStatus() & streamer.RUN_BIT != 0:
                streamer.kill()

    def getStreamer(self, index):
        if index.isValid():
            return self._dllist[index.row()]

    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(str(self._dllist[index.row()]))
            elif role == Qt.DecorationRole:
                # Added Decoration Role to indicate Status...
                _log.debug("DecorationRole role %d" % index.row())
                streamer = self._dllist[index.row()]
                status = streamer.getStatus()
                if status & streamer.ERROR_BIT:
                    return QVariant(self._icon_error)
                elif status & streamer.FIN_BIT:
                    return QVariant(self._icon_fin)
                elif status == streamer.RUN_BIT:
                    return QVariant(self._icon_run)
                else:
                    return QVariant(self._icon_wait)
        return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self._dllist)

    def isSafeToExit(self):
        for streamer in self._dllist:
            if not (streamer.getStatus() & streamer.FIN_BIT):
                return False
        return True

    @pyqtSlot(int)
    def _streamerStatusChanged(self, status):
        _log.debug("status-changed")
        # TRICKEY: test new color management...
        length = len(self._dllist)
        start_idx = self.createIndex(0, 0)
        if length > 0:
            end_idx = self.createIndex(length - 1, 0)
        else:
            end_idx = start_idx
        self.dataChanged.emit(start_idx, end_idx)


class MPStreamer(QObject):

    RUN_BIT = 1
    FIN_BIT = 2
    ERROR_BIT = 4

    _READY = 0
    _RUNNING = RUN_BIT
    _FINISHED_SUC = FIN_BIT
    _FINISHED_ERR = ERROR_BIT | FIN_BIT

    _current_id = 0

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

    def __init__(self, dlinfo, name="worker", mp_path="mplayer", wget="wget"):
        """Creates and initializes a new streamer object.

        :param dlinfo:  Download info container
        :param name:    Optional name of this streamer (This name
                        will be used in debug messages...).
        :param mp_path: Optional path to the mplayer (used to download
                        the stream).
        :param wget:    Optional path to the wget utility (to download
                        the stream).
        """
        QObject.__init__(self)
        self._info = dlinfo
        self._mplayer = mp_path
        self._wget = wget
        self._name = "%s_%02d" % (name, self.nextId())
        self._proc = QProcess()
        self._status = self._READY
        self._lerror = None
        self._doConnections()
        self._play_proc = QProcess()
        self._stream_proc = QProcess()

    def __str__(self):
        return self._info.getFilename()

    def _doConnections(self):
        self._proc.finished.connect(self._qprocessFinished)
        self._proc.stateChanged.connect(self._qprocessStateChanged)

    def _exists(self, filename):
        for i in os.listdir(self._info.destDir):
            basename = splitext(i)[0]
            if filename == basename:
                return True
        return False

    def start(self, overwrite=False, wget=False):
        # TODO: check if path exists and is accessible
        self._lerror = None
        self._info.setExtension(None)
        # remove extension
        if self._status & self.RUN_BIT:
            raise AlreadyRunningError(self._info.getPath())
        elif self._exists(self._info.getFilename()) and (not overwrite):
            raise FileExistsError(self._info.getPath())
        else:
            if self._status & self.FIN_BIT:
                _log.debug("Restarting Download of file '%s'"
                           % self._info.getPath())
            if wget:
                args = ["-c", self._info.getSourceURL(), "-O",
                        self._info.getPath()]
                _log.debug("Starting download using wget (%s)" %
                           " ".join(args))
                self._proc.start(self._wget, args)
            else:
                args = ["-nolirc", "-dumpstream", "-dumpfile",
                        self._info.getPath(), self._info.getSourceURL()]
                _log.debug("Starting download using mplayer (%s)" %
                           " ".join(args))
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
        if self._lerror.find("Failed to open") != -1:
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
                newpath = "%s.%s" % (path, ext)
                _log.debug("Renaming '%s' to '%s'." % (path, newpath))
                os.rename(path, newpath)
                self._info.setExtension(ext)
                succeeded = True

        if self._status != old_status:
            self.changedStatus.emit(self._status)
        self._info.finished.emit(succeeded)

    def playStream(self):
        # TODO:
        # maybe check QProcess::state() should be QProcess::NotRunning
        _log.debug("Trying to start mplayer and play stream")
        self._stream_proc.setStandardInputFile(self._info.getPath())
        self._stream_proc.start(self._mplayer, ["-fs", "-"])

    def playFile(self):
        # TODO:
        # maybe check QProcess::state() should be QProcess::NotRunning
        _log.debug("Trying to start mplayer and play a file")
        args = ["-fs", self._info.getPath()]
        _log.debug("mplayer start argument: %s" % str(args))
        self._play_proc.start(self._mplayer, args)

    def getSize(self, inc_unit=False):
        path = self._info.getPath()
        try:
            size = getsize(path)
        except os.error as ex:
            _log.debug("Couldn't retrieve file size for '%s' -> %s"
                       % (path, str(ex)))
        else:
            if inc_unit:
                idx = 0
                for (i, v) in enumerate(_SIZE_MAX):
                    if (size // v) > 0:
                        return u"%d %s" % ((size / v), _SIZE_PREFIX[i])

    def kill(self):
        self._proc.kill()

    def discard(self):
        self._info.removed.emit()

    def getStatus(self):
        return self._status


if __name__ == '__main__':
    pass

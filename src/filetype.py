import logging
from os.path import exists
from PyQt4.QtCore import (QObject, pyqtSlot, pyqtSignal, QProcess, Qt)

__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


_log = logging.getLogger(__name__)


class FileTypeException(Exception):
    pass


class InvalidPathError(FileTypeException):
    
    def __init__(self, path):
        self.path = path


class ExternalProgramError(FileTypeException):
    pass


class ExtGuesser(object):
    
    _TAVI = "AVI"
    _MMP4 = "video/mp4"
    _MFLV = "video/x-flv"
    _TFLV = "Macromedia Flash Video"
    
    def __init__(self, path):
        self._path = path
        self._proc = QProcess()
        if not exists(self._path):
            raise InvalidPathError(path)
    
    def _guessExtension(self, text, mime):
        if text.find(self._TAVI) >= 0:
            return 'avi'
        elif mime.find(self._MMP4) >= 0:
            return 'mp4'
        elif ((mime.find(self._MFLV) >= 0) and 
              (text.find(self._TFLV) >= 0)):
            return 'flv'
        else:
            return 'unk'
    
    def get(self):
        self._proc.start("file", ["-b", self._path])
        ret0 = self._proc.waitForFinished()
        textual = str(self._proc.readAllStandardOutput())
        self._proc.start("file", ["-bi", self._path])
        ret1 = self._proc.waitForFinished()
        mime = str(self._proc.readAllStandardOutput())
        if ret0 and ret1:
            return self._guessExtension(textual, mime)
        else:
            raise ExternalProgramError()

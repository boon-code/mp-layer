import logging
from PyQt4.QtCore import (QObject, pyqtSlot, pyqtSignal, QProcess, Qt)


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


_log = logging.getLogger(__name__)


class FileTypeException(Exception):
    pass


class InvalidPathException(FileTypeException):
    
    def __init__(self, path):
        self.path = path


def ExtGuesser(QObject):
    
    _TAVI = "AVI"
    _MMP4 = "video/mp4"
    _MFLV = "video/x-flv"
    _TFLV = "Macromedia Flash Video"
    
    
    def __init__(self, path):
        QObject.__init__(self)
        self._path = path
        self._proc = QProcess()
        self._proc.finished.connect(self._finished)
    
    def _getExtension(self, text, mime):
        if text.find(self._TAVI) >= 0:
            return "avi"
        elif mime.find(self._MMP4) >= 0:
            return "mp4"
        elif ((mime.find(self._MFLV) >= 0) and 
              (text.find(self._TFLV) >= 0)):
            return "flv"
        else:
            return "unk"
    
    def __call__(self):
        self._proc.start("file", ["-b", path])
        ret0 = self._proc.waitForFinished()
        textual = self._proc.readAllStandardOutput()
        self._proc.start("file", ["-bi", path])
        ret1 = self._proc.waitForFinished()
        mime = self._proc.readAllStandardOutput()
        if ret0 and ret1:
            return self._getExtension(textual, mime)
        else:
            # TODO: raise an Exception
            pass

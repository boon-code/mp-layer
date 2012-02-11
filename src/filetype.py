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
    
    def __init__(self, path):
        QObject.__init__(self)
        self._path = path
        self._proc = QProcess()
    
    def _doConnections(self):
        pass
    
    def __call__(self):
        pass

import logging
from PyQt4.QtGui import (QPlainTextEdit, QApplication, QMainWindow,
                         QMessageBox)
from PyQt4.QtCore import Qt, pyqtSignal, QString, QEvent, pyqtSlot


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


class UrlEdit(QPlainTextEdit):
    
    pasteText = pyqtSignal(QString)
    
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self._clipboard = QApplication.clipboard()
    
    def event(self, event):
        if ((event.type() == QEvent.KeyPress) and 
                    (event.key() == Qt.Key_V) and
                    (event.modifiers() & Qt.CTRL)):
            self.pasteText.emit(self._clipboard.text())
            return True
        else:
            return QPlainTextEdit.event(self, event)


class MyMainWindow(QMainWindow):
    
    _log = logging.getLogger("%s.MyMainWindow" % __name__)
    _exitMessage = "There are unfinished streams in download queue, \
really exit?"
    
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self._close = True
    
    @pyqtSlot(bool)
    def setEnableClose(self, value):
        if value:
            self._log.debug("Enable closing...")
            self._close = True
        else:
            self._log.debug("Disable closing...")
            self._close = False
    
    def closeEvent(self, event):
        if self._close:
            self._log.debug("Closing main window...")
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Exit Application?',
                    self._exitMessage, QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._log.debug("Ignore unfinished streams and close...")
                event.accept()
            else:
                event.ignore()
                self._log.debug("Abort exit...")

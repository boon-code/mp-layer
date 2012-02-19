from PyQt4.QtGui import QPlainTextEdit, QApplication
from PyQt4.QtCore import Qt, pyqtSignal, QString, QEvent


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

from PyQt4.QtGui import QPlainTextEdit

class UrlEdit(QPlainTextEdit):
    
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)

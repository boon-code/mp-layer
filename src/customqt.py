from PyQt4.QtGui import QPlainTextEdit


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"


class UrlEdit(QPlainTextEdit):
    
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)

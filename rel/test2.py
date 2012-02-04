import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class A(QObject):
    
    succeeded = pyqtSignal()
    
    def __init__(self, a):
        QObject.__init__(self)
        self.a = a
    
    def test(self):
        self.succeeded.emit()

class B(A):
    
    def __init__(self, c):
        A.__init__(self, c + 3)
        self.c = c
        self.succeeded.connect(self.hasSucceeded)
    
    @pyqtSlot()
    def hasSucceeded(self):
        print "Succeeded!", self.a, self.c

a = B(7)
a.test()

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

class AppKiller(QObject):
    
    kill = pyqtSignal()
    
    def __init__(self, time):
        QObject.__init__(self)
        self._timer = QTimer()
        self._num = time
        self._timer.timeout.connect(self.killerSlot)
        self._timer.start(1000)
    
    @pyqtSlot()
    def killerSlot(self):
        self._num -= 1
        if self._num <= 0:
            self._timer.stop()
            self.kill.emit()
        else:
            print "Counting down..."

app = QApplication([])
a = B(7)
a.test()
b = AppKiller(5)
b.kill.connect(app.quit)

app.exec_()

del a
del b
del app

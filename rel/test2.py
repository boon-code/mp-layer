import sys
import time
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
        self._timer.start(2000)
    
    @pyqtSlot()
    def killerSlot(self):
        self._num -= 1
        if self._num <= 0:
            self._timer.stop()
            self.kill.emit()
        else:
            print "Counting down..."

class C(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self._t1 = QTimer()
        self._t2 = QTimer()
        self._t1.timeout.connect(self.slot1)
        self._t2.timeout.connect(self.slot2)
        self._t1.start(1000)
        self._t2.start(10)
        self._dis = False
        self._num = 0
    
    @pyqtSlot()
    def slot1(self):
        print "slot1 started"
        time.sleep(2)
        if not self._dis:
            print "Disconnecting!"
            self._dis = True
            self._t2.stop()
            #self._t2.timeout.disconnect(self.slot2)
        print "slot1 finished"
    
    @pyqtSlot()
    def slot2(self):
        print "slot2 - %d" % self._num
        self._num += 1
    
    def quit(self):
        self._t1.stop()
        self._t2.stop()
    

app = QApplication([])
#a = B(7)
#a.test()
b = AppKiller(5)
b.kill.connect(app.quit)
c = C()



app.exec_()
c.quit()

del b
del c
del app

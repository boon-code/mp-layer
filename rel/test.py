import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Model(QAbstractListModel):
    
    testSig = pyqtSignal()
    
    def testSlot(self, *args):
		print "TestSig caught", args
    
    def __init__(self, data):
        QAbstractListModel.__init__(self, parent=None)
        self.listdata = data
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)
    
    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()
    
    def changedCurrentIndex(self, sel_index, des_index):
        print "Index changed", sel_index, des_index
        print "selected items:", 
        for selitem in sel_index:
            for index in selitem.indexes():
                print index.row(), 
        print ""
        print "deselect items:",
        for deselitem in des_index:
            for index in deselitem.indexes():
                print index.row(),
        print ""


class Bla(QWidget):
    
    uselessSig = pyqtSignal()
    
    def __init__(self):
        QWidget.__init__(self)
        
        lm = Model([1,2,3,4,5])
        pb = QPushButton()
        pb.setText("Bla")
        
        lv = QListView()
        lv.setModel(lm)
        sm = lv.selectionModel();
        
        ret = QObject.connect(sm, SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                        lm.changedCurrentIndex)
        print "BOUND", ret
        
        ret = QObject.connect(pb, SIGNAL("clicked()"), sm, SLOT("clearSelection()"))
        print "BOUND", ret
        
        lm.testSig.connect(lm.testSlot)
        QObject.connect(self, SIGNAL("uselessSig()"), lm, SIGNAL("testSig()"))
        
        ret = QObject.connect(pb, SIGNAL("clicked()"), self, SIGNAL("uselessSig()"))
        print "BOUND", ret
        
        #QObject.connect(self, SIGNAL("uselessSig()"), self.test)
        self.uselessSig.connect(self.test)
        
        layout = QVBoxLayout()
        layout.addWidget(lv)
        layout.addWidget(pb)
        self.setLayout(layout)
    
    def test(self, *args):
        print "Test Trigger"


def main():
    app = QApplication(sys.argv)
    w = Bla()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

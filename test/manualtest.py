#!/usr/bin/env python


import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from os.path import split, normpath, join

def testInteractive():
    import mpl
    import PyQt4.QtCore as core
    import PyQt4.QtGui as gui
    app = gui.QApplication(sys.argv)
    gui.qApp = app
    c = mpl.Controller()
    c.show()
    n = c.nameStorage
    for i in range(1,100):
        s = n.getOrCreateSeries("Serie%d" % i)
    ret = app.exec_()
    del c
    del app
    sys.exit(ret)


def main():
    testInteractive()


if __name__ == '__main__':
    base = split(sys.argv[0])[0]
    path = normpath(join(base, "../src/"))
    sys.path.insert(0, path)
    main()

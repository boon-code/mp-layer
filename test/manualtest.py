#!/usr/bin/env python


import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from os.path import split, normpath, join

def testNaming():
    import naming as n
    a = n.Series("Onkel-Bla")
    b = a.createInstance("url://somewhere", 1, 1)
    b.succeeded.emit()


def main():
    testNaming()


if __name__ == '__main__':
    base = split(sys.argv[0])[0]
    path = normpath(join(base, "../src/"))
    sys.path.insert(0, path)
    main()

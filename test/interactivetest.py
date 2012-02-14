import sys
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from os.path import split, normpath, join
base = split(sys.argv[0])[0]
path = normpath(join(base, "../src/"))
sys.path.insert(0, path)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from download import MPStreamer

a = QApplication([])
b = MPStreamer("url",
               "file")

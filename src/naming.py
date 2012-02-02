from PyQt4.QtCore import QObject
from download import DownloadInfo
import logging


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2011 Manuel Huber."
__license__ = 'GPLv3'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"

_log = logging.getLogger(__name__)


class SeriesInstance(DownloadInfo):
    
    def __init__(self, series, season, episode):
        DownloadInfo.__init__(self, 

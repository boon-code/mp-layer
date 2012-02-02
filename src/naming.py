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
    
    _TNAME = "%s.S%2dE%2d"
    _DBG_SUCCESS = "Download of file '%s' has been successful."
    
    def __init__(self, url, series, season, episode):
        filename = self._TNAME % (series.name, season, episode)
        DownloadInfo.__init__(self, url, filename)
        self._series = series
        self._episode = episode
        self._season = season
    
    def hasSucceeceded(self):
        _log.debug(self._DBG_SUCCESS % self.getFilename())
        self._series.addToHistory(self._season, self._episode)

class Series(object):
    
    def __init__(self, name, curr_season=1, curr_episode=0):
        self.name = name
        self.currentSeason = curr_season
        self.currentEpisode = curr_episode
        self.accessPriority = 0

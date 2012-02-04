from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSlot, QAbstractListModel)
from download import DownloadInfo
import logging
import copy
import json


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2011 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '0.0.0'
__docformat__ = "restructuredtext en"

_log = logging.getLogger(__name__)


class SeriesInstance(DownloadInfo):
    
    _TNAME = "%s.S%02dE%02d"
    _DBG_SUCCESS = "Download of file '%s' has been successful."
    
    def __init__(self, url, series, season, episode):
        filename = self._TNAME % (series.name, season, episode)
        DownloadInfo.__init__(self, url, filename)
        self._series = series
        self._episode = episode
        self._season = season
        self.succeeded.connect(self.hasSucceeded)
    
    @pyqtSlot()
    def hasSucceeded(self):
        _log.debug(self._DBG_SUCCESS % self.getFilename())
        self._series.addToHistory(self._season, self._episode)


class Series(object):
    
    def __init__(self, name, curr_season=1, curr_episode=0):
        self.name = name
        self.currentSeason = curr_season
        self.currentEpisode = curr_episode
        self.accessPriority = 0
        self._history = dict()
    
    def createInstance(self, url, season, episode):
        inst = SeriesInstance(url, self, season, episode)
        return inst
    
    def addToHistory(self, season, episode):
        _log.info("Adding episode %d of season %d (series: '%s')."
                  % (episode, season, self.name))
        if season not in self._history:
            _log.debug("Creating entry for season %d (series: '%s')."
                       % (season, self.name))
            self._history[season] = set()
        if episode in self._history[season]:
            _log.debug("'%s.S%02d.E%02d' already in history"
                       % (self.name, season, episode))
        else:
            _log.debug("Adding '%s.S%02d.E%02d' to history"
                       % (self.name, season, episode))
            self._history[season].add(episode)
    
    def mergeData(self, data):
        for (season, epilist) in data.items():
            if season not in self._history:
                _log.debug("Adding full season %d (series: '%s')."
                           % (season, self.name))
                self._history[season] = set(epilist)
            else:
                diff = self._history[season].difference(epilist)
                _log.debug("Adding [%s] (season: %d, series: '%s')."
                           % (", ".join((str(i) for i in diff)),
                              season, self.name))
                self._history[season].update(diff)
    
    def getData(self):
        return copy.deepcopy(self._history)


class SeriesStorage(QAbstractListModel):
    
    def __init__(self):
        QAbstractListModel.__init__(self, None)
        self._series = dict()
    
    def load(self, path):
        with open(path, "r") as f:
            return json.load(f)
    
    def store(self, path):
        with open(path, "w") as f:
            json.dump(objs, f)
    
    def get(self, index):
        pass
    
    def find(self, name):
        return (False, None)
    
    def getOrCreateSeries(self, name):
        pass
    
    
    
    


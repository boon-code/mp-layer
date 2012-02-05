from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, 
                          pyqtSlot, QAbstractListModel, QModelIndex)
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


class NamingException(Exception):
    pass


class WrongJSOError(NamingException):
    
    def __init__(self, name, wtype):
        self.name = name
        self.wtype = wtype
    
    def __str__(self):
        return "JSO '%s' is of type '%s'" % (str(self.name),
                                             str(self.wtype))


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
    
    _WRN_LDSKIP = "Skipping season %d (series: '%s'); Illegal list format."
    _WRN_ILLSEASON = "Skipping illegal season value '%s'"
    _DBG_SKIP = "Skipping cause of exception '%s'."
    
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
            try:
                season = int(season)
            except TypeError as ex:
                _log.debug(self._DBG_SKIP % str(ex))
                _log.warning(self._WRN_ILLSEASON % str(season))
                continue
            try:
                epi = set((int(i) for i in epilist))
            except TypeError as ex:
                _log.debug(self._DBG_SKIP % str(ex))
                _log.warning(self._WRN_LDSKIP % (season, self.name))
                continue
            if season not in self._history:
                _log.debug("Adding full season %d (series: '%s')."
                           % (season, self.name))
                self._history[season] = epi
            else:
                diff = self._history[season].difference(epi)
                _log.debug("Adding [%s] (season: %d, series: '%s')."
                           % (", ".join((str(i) for i in diff)),
                              season, self.name))
                self._history[season].update(diff)
    
    def getData(self):
        return copy.deepcopy(self._history)


class SeriesStorage(QAbstractListModel):
    
    _WRN_LAST = "Couldn't load last season, episode from '%s' \
(found type '%s')."
    _WRN_SKIPENTRY = "Skipped entry because of '%s' (having type '%s')."
    
    def __init__(self):
        QAbstractListModel.__init__(self, None)
        self._series = dict()
    
    def _loadFile(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    
    def _tryLoadLast(self, name, obj):
        
        if 'last' in obj:
            if not isinstance(obj['last'], list):
                raise WrongJSOError("%s.last" % name,
                                    type(obj['last']))
            last = (obj['last'][0], obj['last'][1])
            if (not isinstance(last[0], int):
                raise WrongJSOError("%s.last[0](season)" % name,
                                    type(last[0]))
            elif (not isinstance(last[1], int):
                raise WrongJSOError("%s.last[1](episode)" % name,
                                    type(last[1]))
            else:
                return last
    
    def _tryLoadEntry(self, name, obj):
        
        last = None
        try:
            last = self._tryLoadLast(name, obj)
        except WrongJSOError as ex:
            _log.warning(self._WRN_LAST % (str(ex.name), str(ex.wtype))
        
        if 'history' in obj:
            if not isinstance(obj['history'], dict):
                raise WrongJSOError("%s.history" % name,
                                    type(obj['history']))
            if name in self._series:
                self._series[name].mergeData(obj['history'])
            else:
                self._series[name] = Series(name)
        if last is not None:
            self._series[name].currentSeason = last[0]
            self._series[name].currentEpisode = last[1]
    
    def load(self, path):
        jobj = self._loadFile(path)
        if not isinstance(jobj, dict):
            raise WrongJSOError("root", type(jobj))
        
        for (name, obj) in jobj.items():
            try:
                if not isinstance(name, str):
                    raise WrongJSOError("name", type(name))
                if not isinstance(obj, dict):
                    raise WrongJSOError(name, type(obj))
                
                self._tryLoadEntry(name, obj)
            except WrongJSOError as ex:
                _log.warning(self._WRN_SKIPENTRY % (str(ex.name),
                                                    str(ex.wtype)))
    
    def store(self, path):
        jobj = dict()
        # TODO: continue here!
        for (name, series) in self._series:
            pass
        with open(path, "w") as f:
            json.dump(self._series, f)
    
    def get(self, index):
        pass
    
    def find(self, name):
        return (False, None)
    
    def getOrCreateSeries(self, name):
        pass
    
    def data(self, index, role):
        pass
    
    def rowCount(self, parent=QModelIndex()):
        pass
    
    
    
    


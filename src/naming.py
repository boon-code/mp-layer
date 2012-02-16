from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSignal, 
                          pyqtSlot, QAbstractListModel, QModelIndex,
                          Qt, QVariant)
from download import DownloadInfo
import logging
import copy
import json


__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
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
    _WRN_FAILURE = "Download of file '%s' has failed."
    
    changedStatus = pyqtSignal()
    
    def __init__(self, url, series, season, episode):
        filename = self._TNAME % (series.name, season, episode)
        DownloadInfo.__init__(self, url, filename)
        self._series = series
        self.episode = episode
        self.season = season
        self.finished.connect(self.hasFinished)
        self.removed.connect(self.removeInstance)
    
    def getName(self):
        return self._series.name
    
    @pyqtSlot('bool')
    def hasFinished(self, succeeded):
        if succeeded:
            _log.debug(self._DBG_SUCCESS % self.getFilename())
        else:
            _log.warning(self._WRN_FAILURE % self.getFilename())
        # Tell Series class about it (in either case)
        self._series.finishedInstance(self, succeeded)
    
    @pyqtSlot()
    def removeInstance(self):
        _log.debug("Removed instance %s" % self.getFilename())
        self._series.removedInstance(self)


class Series(QObject):
    
    _WRN_LDSKIP = "Skipping season %d (series: '%s'); Illegal list format."
    _WRN_ILLSEASON = "Skipping illegal season value '%s'"
    _WRN_LAST = "Couldn't load last season, episode from '%s' \
(found type '%s')."
    _DBG_SKIP = "Skipping cause of exception '%s'."
    
    changedHistory = pyqtSignal()
    
    def __init__(self, name, curr_season=1, curr_episode=0):
        QObject.__init__(self)
        self.name = name
        self.currentSeason = curr_season
        self.currentEpisode = curr_episode
        self.accessPriority = 0
        self._history = dict()
        # DESC: (season, episode) will be added to this set if
        #       an instance has been created to prevent multiple
        #       downloads of the same file...
        self._instances = set()
    
    def createInstance(self, url, season, episode):
        entry = (int(season), int(episode))
        if entry not in self._instances:
            _log.debug("created instance '%s.S%02dE%02d'."
                        % (self.name, season, episode))
            self._instances.add(entry)
            inst = SeriesInstance(str(url), self, int(season), int(episode))
            return inst
        else:
            _log.info("'%s.S%02dE%02d' is being downloaded."
                      % (self.name, season, episode))
    
    def finishedInstance(self, instance, succeeded):
        season = instance.season
        episode = instance.episode
        if succeeded:
            self._addToHistory(season, episode)
        else:
            # ensure that element is not in history
            if self.inHistory(season, episode):
                self._removeFromHistory(season, episode)
        self.changedHistory.emit()
    
    def removedInstance(self, instance):
        entry = (instance.season, instance.episode)
        self._instances.discard(entry)
        _log.debug("Removed S%02dE%02d from instance list." % entry)
        self.changedHistory.emit()
    
    def _removeFromHistory(self, season, episode):
        if self.inHistory(season, episode):
            _log.info("Removing '%s.S%02dE%02d' from history!")
            self._history[season].remove(episode)
    
    def _addToHistory(self, season, episode):
        _log.info("Adding episode %d of season %d (series: '%s')."
                  % (episode, season, self.name))
        if season not in self._history:
            _log.debug("Creating entry for season %d (series: '%s')."
                       % (season, self.name))
            self._history[season] = set()
        if episode in self._history[season]:
            _log.debug("'%s.S%02dE%02d' already in history"
                       % (self.name, season, episode))
        else:
            _log.debug("Adding '%s.S%02dE%02d' to history"
                       % (self.name, season, episode))
            self._history[season].add(episode)
    
    def _tryLoadLast(self, obj):
        if 'last' in obj:
            if not isinstance(obj['last'], list):
                raise WrongJSOError("%s.last" % self.name,
                                    type(obj['last']))
            last = (obj['last'][0], obj['last'][1])
            if not isinstance(last[0], int):
                raise WrongJSOError("%s.last[0](season)" % self.name,
                                    type(last[0]))
            elif not isinstance(last[1], int):
                raise WrongJSOError("%s.last[1](episode)" % self.name,
                                    type(last[1]))
            else:
                return last
    
    def _mergeHistory(self, history):
        for (season, epilist) in history.items():
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
    
    def inHistory(self, season, episode):
        season = int(season)
        episode = int(episode)
        if season in self._history:
            if episode in self._history[season]:
                return True
        return False
    
    def inProgress(self, season, episode):
        entry = (int(season), int(episode))
        if entry in self._instances:
            return True
        else:
            return False
    
    def mergeData(self, data):
        try:
            self._tryLoadLast(data)
            self.currentSeason = last[0]
            self.currentEpisode = last[1]
        except WrongJSOError as ex:
            _log.warning(self._WRN_LAST % (str(ex.name), str(ex.wtype)))
        if 'history' in data:
            history = data['history']
            if not isinstance(history, dict):
                raise WrongJSOError("%s.history" % self.name,
                                    type(history))
            self._mergeHistory(history)
    
    def _normalizeHistory(self):
        rm_list = list()
        for (season, eps) in self._history.items():
            if len(eps) == 0:
                rm_list.append(season)
        for i in rm_list:
            self._history.pop(i, None)
    
    def getData(self):
        obj = dict()
        self._normalizeHistory()
        obj['history'] = copy.deepcopy(self._history)
        obj['last'] = (self.currentSeason, self.currentEpisode)
        return obj


class SeriesStorage(QAbstractListModel):
    
    _WRN_SKIPENTRY = "Skipped entry because of '%s' (having type '%s')."
    
    def __init__(self):
        QAbstractListModel.__init__(self, None)
        self._series = list()
        self._idbyname = dict()
    
    def _addSeries(self, name):
        name = str(name)
        series = Series(name)
        self._series.append(series)
        index = self._series.index(series)
        self._idbyname[name] = index
        self.reset()
        return index
    
    def _loadFile(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    
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
                
                if name not in self._idbyname:
                    self._addSeries(name)
                self.mergeData(obj)
            except WrongJSOError as ex:
                _log.warning(self._WRN_SKIPENTRY % (str(ex.name),
                                                    str(ex.wtype)))
    
    def store(self, path):
        jobj = dict()
        for series in self._series:
            jobj[series.name] = series.getData()
        with open(path, 'w') as f:
            json.dump(self._series, f)
    
    def get(self, index):
        if index.isValid():
            return self._series[index.row()]
    
    def find(self, name):
        name = str(name)
        if name in self._idbyname:
            # column is not used => 0
            index = self.createIndex(self._idbyname[name], 0)
            return (True, index)
        else:
            return (False, None)
    
    def getOrCreateSeries(self, name):
        name = unicode(name)
        if name in self._idbyname:
            index = self._idbyname[name]
        else:
            index = self._addSeries(name)
        return self.createIndex(index, 0)
    
    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self._series[index.row()].name)
        else:
            return QVariant()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._series)

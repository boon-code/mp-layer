#!/usr/bin/env python

import sys
import os
import optparse
import logging

_DEFAULT_LOG_FORMAT = "%(name)s : %(threadName)s : %(levelname)s \
: %(message)s"
logging.basicConfig(stream=sys.stderr, format=_DEFAULT_LOG_FORMAT
     , level=logging.DEBUG)

from PyQt4.QtCore import (QObject, SIGNAL, SLOT, pyqtSlot, Qt,
                          pyqtSignal, QString, QModelIndex, QTimer)
from PyQt4.QtGui import (QItemSelection, QMainWindow, QApplication,
                         QItemSelectionModel, qApp, QMessageBox,
                         QSortFilterProxyModel, QCompleter)
from PyQt4 import QtGui
from gui import Ui_MPLayerGui
from customqt import MyMainWindow
from os.path import isdir, join
from datetime import datetime
import naming
import download

_log = logging.getLogger(__name__)

__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2012 Manuel Huber."
__license__ = 'GPLv2'
__version__ = '1.1.0'
__docformat__ = "restructuredtext en"


STORAGE_FILE = "mpl-storage.json"
# default storage file name...

DL_PATH = os.getcwd()
STORAGE_PATH = join(os.getcwd(),STORAGE_FILE)


class EpisodeController(QObject):

    nextEpisode = pyqtSignal(int)
    currentSeason = pyqtSignal(int)

    def __init__(self, controller):
        QObject.__init__(self)
        self._ctrl = controller
        self._nameStorage = controller.nameStorage
        self._dlList = controller.dlList
        self._ui = controller.ui
        self._selModel = self._ui.lvSeries.selectionModel()
        self._ui.pubAddEpisode.setEnabled(False)

    def _select_item(self, index):
        filtered_index = self._ctrl._filter_model.mapFromSource(index)
        self._selModel.setCurrentIndex(filtered_index,
                                       QItemSelectionModel.SelectCurrent)

    def _src_index(self, index=None):
        if index is None:
            index = self._selModel.currentIndex()
        return self._ctrl._filter_model.mapToSource(index)

    def doConnections(self):
        ui = self._ui
        ui.ledEName.textChanged.connect(self._changedEpisodeName)
        ui.spnEpisode.valueChanged.connect(self._updateEpisodeControls)
        ui.spnSeason.valueChanged.connect(self._updateEpisodeControls)
        self._ctrl.changedURL.connect(self._updateEpisodeControls)
        ui.pubAddEpisode.clicked.connect(self.addEpisode)
        model = self._selModel
        model.currentChanged.connect(self._selectedEpisodeChanged)

    @pyqtSlot(QModelIndex, QModelIndex)
    def _selectedEpisodeChanged(self, sel, desl):
        """Slot will be called if selected index changes...

        :param sel:  New selection (can be invalid)
        :param desl: Old selection (can be invalid)
        """
        series = self._nameStorage.get(self._src_index(sel))
        if series is not None:
            self._ui.ledEName.setText(series.name)

    @pyqtSlot(QString)
    def _changedEpisodeName(self, text):
        """Slot will be called if new episode name has been typed in.

        :param text: new text.
        """
        ret, index = self._nameStorage.find(text)
        if ret:
            self._select_item(index)
        else:
            self._selModel.clear()
        self._updateEpisodeControls()

    def _isEpisodeInProgress(self):
        """Checks if current episode is being downloaded.

        :returns: True if episode is downloading else False.
        """
        series = self._nameStorage.get(self._src_index())
        if series is not None:
            season = self._ui.spnSeason.value()
            episode = self._ui.spnEpisode.value()
            return series.inProgress(season, episode)
        else:
            return False

    @pyqtSlot()
    def _updateEpisodeControls(self):
        text = u""
        enabled = False
        ui = self._ui
        if not ui.ledEName.text().isEmpty():
            series = self._nameStorage.get(self._src_index())
            if series is not None:
                season = ui.spnSeason.value()
                episode = ui.spnEpisode.value()
                if series.inProgress(season, episode):
                    text = u"Has already been added to list!"
                    enabled = False
                elif series.inHistory(season, episode):
                    text = u"Has already been downloaded once!"
            if self._ctrl.valid_url:
                enabled = True
        if self._ui.pubAddEpisode.isEnabled != enabled:
            self._ui.pubAddEpisode.setEnabled(enabled)
        ui.labEInstance.setText(text)

    @pyqtSlot()
    def addEpisode(self):
        name = self._ui.ledEName.text()
        if not name.isEmpty():
            index = self._nameStorage.getOrCreateSeries(name)
            self._ctrl._updateList()
            series = self._nameStorage.get(index)
            self._select_item(index)
            ui = self._ui
            season = ui.spnSeason.value()
            episode = ui.spnEpisode.value()
            if not series.inProgress(season, episode):
                inst = series.createInstance(ui.pteUrl.toPlainText(),
                                             season, episode)
                series.changedHistory.connect(self._updateEpisodeControls)
                self._updateEpisodeControls()
                self._ctrl.download(inst)
                # TODO: increment to next episode...


class Controller(QObject):

    changedURL = pyqtSignal()

    def __init__(self, dl_path=DL_PATH, store_file=STORAGE_PATH,
                 autostart=True):
        QObject.__init__(self)
        self._gui = MyMainWindow()
        self._autostart = autostart
        self._dlpath = dl_path
        self._store_file = store_file
        self.ui = Ui_MPLayerGui()
        self.ui.setupUi(self._gui)
        self.dlList = download.DownloadList()
        self.nameStorage = naming.SeriesStorage()
        self.valid_url = False
        self._timer = QTimer()
        self._timeout = 500
        # init-settings
        self.ui.pubAddSimple.setEnabled(False)
        self.ui.pubStart.setEnabled(False)
        self.ui.pubKill.setEnabled(False)
        self.ui.pubRemove.setEnabled(False)

        self._filter_model = QSortFilterProxyModel()
        self._filter_model.setSourceModel(self.nameStorage)
        self.ui.lvSeries.setModel(self._filter_model)
        self._epiController = EpisodeController(self)
        self.ui.lvDownloads.setModel(self.dlList)
        self._selDM = self.ui.lvDownloads.selectionModel()
        self._gui.setExitChecker(self._isSafeToExit)
        self._doConnections()
        self._loadHistory()
        # completion
        self._completer = QCompleter()
        self._completer.setModel(self._filter_model)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setCompletionRole(Qt.DisplayRole)
        self.ui.ledEName.setCompleter(self._completer)

    def _isSafeToExit(self):
        return self.dlList.isSafeToExit()

    def _updateList(self):
        self._filter_model.sort(0)

    def _loadHistory(self):
        try:
            self.nameStorage.load(self._store_file)
            self._updateList()
        except IOError as ex:
            _log.info("Couldn't load history: '%s'" % str(ex))

    @pyqtSlot()
    def _storeHistory(self):
        self.nameStorage.store(self._store_file)

    def _doConnections(self):
        self.ui.pteUrl.textChanged.connect(self._changedURL)
        self.ui.ledMName.textChanged.connect(self._updateSimpleButton)
        self._epiController.doConnections()
        self.changedURL.connect(self._updateSimpleButton)
        self._selDM.currentChanged.connect(self._selectedDLChanged)
        self.ui.pubAddSimple.clicked.connect(self._addSimple)
        self.ui.pubRemove.clicked.connect(self._removeDownload)
        self.ui.pubStart.clicked.connect(self._startDownload)
        self.ui.pubKill.clicked.connect(self._killDownload)
        self._timer.timeout.connect(self._updateDlSelection)
        self.ui.pteUrl.pasteText.connect(self.ui.pteUrl.setPlainText)
        self.ui.pubMplayer.clicked.connect(self._playStream)
        qApp.aboutToQuit.connect(self._storeHistory)

    @pyqtSlot(bool)
    def setAutostart(self, autostart):
        self._autostart = autostart

    @pyqtSlot(QString)
    def setDLPath(self, path):
        path = str(path)
        if isdir(path):
            self._dlpath = path
            _log.debug("Setting Download Path to '%s'." % path)
        else:
            _log.warning("'%s' isn't a directory" % path)

    @pyqtSlot()
    def _changedURL(self):
        """URL has been changed.

        This slot checks if the url widget is empty, and
        sends out a signal if the empty status changed since
        the last message.
        """
        url_empty = self.ui.pteUrl.toPlainText().isEmpty()
        if url_empty and self.valid_url:
            self.valid_url = False
            self.changedURL.emit()
        elif (not url_empty) and (not self.valid_url):
            self.valid_url = True
            self.changedURL.emit()

    @pyqtSlot()
    def _updateSimpleButton(self):
        """This slot checks if simple download button should be enabled.

        This slot reads the valid_url member and checks the current
        status (empty?) of the LineEdit ledMName.
        """
        enabled = False
        if self.valid_url and not self.ui.ledMName.text().isEmpty():
            enabled = True
        if self.ui.pubAddSimple.isEnabled != enabled:
            self.ui.pubAddSimple.setEnabled(enabled)

    def _updateDlSelection(self):
        start = False
        kill = False
        remove = False
        catstream = False
        text = u"Select an item for more information..."
        index = self._selDM.currentIndex()
        size_str = u""
        streamer = self.dlList.getStreamer(index)
        if streamer is not None:
            status = streamer.getStatus()
            if status & streamer.RUN_BIT:
                size = streamer.getSize(inc_unit=True)
                if size is not None:
                    size_str = u"Current size: %s" % size
                kill = True
                catstream = True
                text = u"Download in progress..."
            elif status & streamer.FIN_BIT:
                size = streamer.getSize(inc_unit=True)
                if size is not None:
                    size_str = u"Current size: %s" % size
                if status & streamer.ERROR_BIT:
                    start = True
                    text = u"Download failed..."
                else:
                    catstream = True
                    text = u"Download successful!"
                remove = True
            else:
                text = u"Ready"
                start = True
                remove = True
        self.ui.pubStart.setEnabled(start)
        self.ui.pubKill.setEnabled(kill)
        self.ui.pubRemove.setEnabled(remove)
        self.ui.pubMplayer.setEnabled(catstream)
        self.ui.labStatus.setText(text)
        self.ui.labSize.setText(size_str)

    @pyqtSlot(QModelIndex, QModelIndex)
    def _selectedDLChanged(self, sel, desl):
        streamer = self.dlList.getStreamer(sel)
        if streamer is not None:
            streamer.changedStatus.connect(self._updateDlSelection)
            self._timer.start(self._timeout)
        else:
            self._timer.stop()
        self._updateDlSelection()

    @pyqtSlot()
    def _startDownload(self):
        index = self._selDM.currentIndex()
        self._startSpecificStream(index)

    @pyqtSlot()
    def _killDownload(self):
        index = self._selDM.currentIndex()
        streamer = self.dlList.getStreamer(index)
        if streamer is not None:
            streamer.kill()

    @pyqtSlot()
    def _removeDownload(self):
        index = self._selDM.currentIndex()
        streamer = self.dlList.getStreamer(index)
        if streamer is not None:
            streamer.changedStatus.disconnect(self._updateDlSelection)
            self._selDM.clear()
            self.dlList.remove(index)

    def _startSpecificStream(self, index):
        wget = self.ui.chkWgetMode.isChecked()
        try:
            self.dlList.start(index, wget=wget)
        except download.FileExistsError as ex:
            reply = QMessageBox.question(self._gui, 'Overwrite?',
                    "File '%s' exists! Overwrite?" % ex.path,
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.dlList.start(index, overwrite=True, wget=wget)

    def download(self, dlinfo):
        """Add download to list (and eventually start it)

        This method can be used to download
        :param dlinfo: Download information for streamer.
        """
        dlinfo.destDir = self._dlpath
        index = self.dlList.add(dlinfo)
        self._selDM.setCurrentIndex(index,
                QItemSelectionModel.SelectCurrent)
        if self._autostart:
            self._startSpecificStream(index)

    @pyqtSlot()
    def _addSimple(self):
        """Called if a simple download has been enqueued.

        """
        if self.valid_url and not self.ui.ledMName.text().isEmpty():
            url = str(self.ui.pteUrl.toPlainText())
            name = str(self.ui.ledMName.text())
            dlinfo = download.DownloadInfo(url, name, self._dlpath)
            self.download(dlinfo)

    @pyqtSlot()
    def _playStream(self):
        index = self._selDM.currentIndex()
        streamer = self.dlList.getStreamer(index)
        if streamer is not None:
            _log.debug("Trying to play %s" % str(streamer))
            if (streamer.getStatus() & streamer.FIN_BIT):
                streamer.playFile()
            else:
                streamer.playStream()

    def show(self):
        self._gui.show()


def main(argv):
    parser = optparse.OptionParser(
        usage="usage: %prog [options] <settings_file>",
        version=("%prog " + __version__)
    )
    parser.add_option("--verbose", action="store_const", const=logging.DEBUG,
        dest="verb_level", help="Verbose output (DEBUG)"
    )
    parser.add_option("--quiet",
                      action="store_const",
                      const=logging.ERROR,
                      dest="verb_level",
                      help="Non verbose output: only output errors"
    )
    parser.set_defaults(version=False, verb_level=logging.INFO)

    options, args = parser.parse_args(argv)

    logging.root.setLevel(options.verb_level)
    logging.debug("Starting up '%s' (%s)" % (
        os.path.basename(sys.argv[0]),
        datetime.now().isoformat())
    )

    if len(args) == 1:
        path = args[0]
        storepath = join(path, STORAGE_FILE)
        app = QApplication([])
        QtGui.qApp = app
        c = Controller(store_file=storepath)
        c.setDLPath(path)
        c.show()
        ret = app.exec_()
        del c
        del app
        sys.exit(ret)


if __name__ == '__main__':
    main(sys.argv[1:])

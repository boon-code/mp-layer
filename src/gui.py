# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qt4-layout/gui.ui'
#
# Created: Tue Feb  7 19:50:31 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MPLayerGui(object):
    def setupUi(self, MPLayerGui):
        MPLayerGui.setObjectName(_fromUtf8("MPLayerGui"))
        MPLayerGui.resize(915, 600)
        MPLayerGui.setWhatsThis(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MPLayerGui)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.grpDownloadArea = QtGui.QGroupBox(self.centralwidget)
        self.grpDownloadArea.setObjectName(_fromUtf8("grpDownloadArea"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.grpDownloadArea)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.frame = QtGui.QFrame(self.grpDownloadArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.labStatus = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labStatus.sizePolicy().hasHeightForWidth())
        self.labStatus.setSizePolicy(sizePolicy)
        self.labStatus.setMinimumSize(QtCore.QSize(0, 0))
        self.labStatus.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labStatus.setWordWrap(True)
        self.labStatus.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.labStatus.setObjectName(_fromUtf8("labStatus"))
        self.verticalLayout_4.addWidget(self.labStatus)
        self.verticalLayout_5.addWidget(self.frame)
        self.lvDownloads = QtGui.QListView(self.grpDownloadArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvDownloads.sizePolicy().hasHeightForWidth())
        self.lvDownloads.setSizePolicy(sizePolicy)
        self.lvDownloads.setMinimumSize(QtCore.QSize(280, 0))
        self.lvDownloads.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lvDownloads.setObjectName(_fromUtf8("lvDownloads"))
        self.verticalLayout_5.addWidget(self.lvDownloads)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pubStart = QtGui.QPushButton(self.grpDownloadArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pubStart.sizePolicy().hasHeightForWidth())
        self.pubStart.setSizePolicy(sizePolicy)
        self.pubStart.setMinimumSize(QtCore.QSize(140, 0))
        self.pubStart.setObjectName(_fromUtf8("pubStart"))
        self.gridLayout_2.addWidget(self.pubStart, 0, 0, 1, 1)
        self.pubKill = QtGui.QPushButton(self.grpDownloadArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pubKill.sizePolicy().hasHeightForWidth())
        self.pubKill.setSizePolicy(sizePolicy)
        self.pubKill.setMinimumSize(QtCore.QSize(140, 0))
        self.pubKill.setObjectName(_fromUtf8("pubKill"))
        self.gridLayout_2.addWidget(self.pubKill, 0, 1, 1, 1)
        self.pubRemove = QtGui.QPushButton(self.grpDownloadArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pubRemove.sizePolicy().hasHeightForWidth())
        self.pubRemove.setSizePolicy(sizePolicy)
        self.pubRemove.setMinimumSize(QtCore.QSize(140, 0))
        self.pubRemove.setObjectName(_fromUtf8("pubRemove"))
        self.gridLayout_2.addWidget(self.pubRemove, 1, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.horizontalLayout_5.addWidget(self.grpDownloadArea)
        self.grpAddArea = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpAddArea.sizePolicy().hasHeightForWidth())
        self.grpAddArea.setSizePolicy(sizePolicy)
        self.grpAddArea.setObjectName(_fromUtf8("grpAddArea"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.grpAddArea)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox = QtGui.QGroupBox(self.grpAddArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pteUrl = UrlEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pteUrl.sizePolicy().hasHeightForWidth())
        self.pteUrl.setSizePolicy(sizePolicy)
        self.pteUrl.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pteUrl.setObjectName(_fromUtf8("pteUrl"))
        self.verticalLayout.addWidget(self.pteUrl)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.tabNaming = QtGui.QTabWidget(self.grpAddArea)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabNaming.sizePolicy().hasHeightForWidth())
        self.tabNaming.setSizePolicy(sizePolicy)
        self.tabNaming.setObjectName(_fromUtf8("tabNaming"))
        self.tabNameEpisode = QtGui.QWidget()
        self.tabNameEpisode.setObjectName(_fromUtf8("tabNameEpisode"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tabNameEpisode)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lvSeries = QtGui.QListView(self.tabNameEpisode)
        self.lvSeries.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lvSeries.setObjectName(_fromUtf8("lvSeries"))
        self.horizontalLayout_2.addWidget(self.lvSeries)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labEName = QtGui.QLabel(self.tabNameEpisode)
        self.labEName.setObjectName(_fromUtf8("labEName"))
        self.gridLayout.addWidget(self.labEName, 0, 0, 1, 1)
        self.ledEName = QtGui.QLineEdit(self.tabNameEpisode)
        self.ledEName.setObjectName(_fromUtf8("ledEName"))
        self.gridLayout.addWidget(self.ledEName, 0, 1, 1, 1)
        self.labEpisodeTitle = QtGui.QLabel(self.tabNameEpisode)
        self.labEpisodeTitle.setObjectName(_fromUtf8("labEpisodeTitle"))
        self.gridLayout.addWidget(self.labEpisodeTitle, 1, 0, 1, 1)
        self.ledTitle = QtGui.QLineEdit(self.tabNameEpisode)
        self.ledTitle.setObjectName(_fromUtf8("ledTitle"))
        self.gridLayout.addWidget(self.ledTitle, 1, 1, 1, 1)
        self.labSeason = QtGui.QLabel(self.tabNameEpisode)
        self.labSeason.setObjectName(_fromUtf8("labSeason"))
        self.gridLayout.addWidget(self.labSeason, 2, 0, 1, 1)
        self.spnSeason = QtGui.QSpinBox(self.tabNameEpisode)
        self.spnSeason.setObjectName(_fromUtf8("spnSeason"))
        self.gridLayout.addWidget(self.spnSeason, 2, 1, 1, 1)
        self.labEpisode = QtGui.QLabel(self.tabNameEpisode)
        self.labEpisode.setObjectName(_fromUtf8("labEpisode"))
        self.gridLayout.addWidget(self.labEpisode, 3, 0, 1, 1)
        self.spnEpisode = QtGui.QSpinBox(self.tabNameEpisode)
        self.spnEpisode.setObjectName(_fromUtf8("spnEpisode"))
        self.gridLayout.addWidget(self.spnEpisode, 3, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pubAddEpisode = QtGui.QPushButton(self.tabNameEpisode)
        self.pubAddEpisode.setMinimumSize(QtCore.QSize(140, 0))
        self.pubAddEpisode.setObjectName(_fromUtf8("pubAddEpisode"))
        self.horizontalLayout.addWidget(self.pubAddEpisode)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.tabNaming.addTab(self.tabNameEpisode, _fromUtf8(""))
        self.tabNameSimple = QtGui.QWidget()
        self.tabNameSimple.setObjectName(_fromUtf8("tabNameSimple"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabNameSimple)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labMName = QtGui.QLabel(self.tabNameSimple)
        self.labMName.setMinimumSize(QtCore.QSize(0, 0))
        self.labMName.setObjectName(_fromUtf8("labMName"))
        self.horizontalLayout_3.addWidget(self.labMName)
        self.ledMName = QtGui.QLineEdit(self.tabNameSimple)
        self.ledMName.setObjectName(_fromUtf8("ledMName"))
        self.horizontalLayout_3.addWidget(self.ledMName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.pubAddSimple = QtGui.QPushButton(self.tabNameSimple)
        self.pubAddSimple.setMinimumSize(QtCore.QSize(140, 0))
        self.pubAddSimple.setObjectName(_fromUtf8("pubAddSimple"))
        self.horizontalLayout_6.addWidget(self.pubAddSimple)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.tabNaming.addTab(self.tabNameSimple, _fromUtf8(""))
        self.verticalLayout_6.addWidget(self.tabNaming)
        self.horizontalLayout_5.addWidget(self.grpAddArea)
        MPLayerGui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MPLayerGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 915, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MPLayerGui.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MPLayerGui)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MPLayerGui.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MPLayerGui)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MPLayerGui)
        self.tabNaming.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MPLayerGui.close)
        QtCore.QMetaObject.connectSlotsByName(MPLayerGui)

    def retranslateUi(self, MPLayerGui):
        MPLayerGui.setWindowTitle(QtGui.QApplication.translate("MPLayerGui", "MP-Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.grpDownloadArea.setTitle(QtGui.QApplication.translate("MPLayerGui", "Downloads:", None, QtGui.QApplication.UnicodeUTF8))
        self.labStatus.setText(QtGui.QApplication.translate("MPLayerGui", "Current Status", None, QtGui.QApplication.UnicodeUTF8))
        self.pubStart.setText(QtGui.QApplication.translate("MPLayerGui", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.pubKill.setText(QtGui.QApplication.translate("MPLayerGui", "Kill", None, QtGui.QApplication.UnicodeUTF8))
        self.pubRemove.setText(QtGui.QApplication.translate("MPLayerGui", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.grpAddArea.setTitle(QtGui.QApplication.translate("MPLayerGui", "Add new Download:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MPLayerGui", "URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.labEName.setText(QtGui.QApplication.translate("MPLayerGui", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.labEpisodeTitle.setText(QtGui.QApplication.translate("MPLayerGui", "Title [opt.]:", None, QtGui.QApplication.UnicodeUTF8))
        self.labSeason.setText(QtGui.QApplication.translate("MPLayerGui", "Season:", None, QtGui.QApplication.UnicodeUTF8))
        self.labEpisode.setText(QtGui.QApplication.translate("MPLayerGui", "Episode:", None, QtGui.QApplication.UnicodeUTF8))
        self.pubAddEpisode.setText(QtGui.QApplication.translate("MPLayerGui", "Download Stream", None, QtGui.QApplication.UnicodeUTF8))
        self.tabNaming.setTabText(self.tabNaming.indexOf(self.tabNameEpisode), QtGui.QApplication.translate("MPLayerGui", "Episode (Smart Naming)", None, QtGui.QApplication.UnicodeUTF8))
        self.labMName.setText(QtGui.QApplication.translate("MPLayerGui", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pubAddSimple.setText(QtGui.QApplication.translate("MPLayerGui", "Download Stream", None, QtGui.QApplication.UnicodeUTF8))
        self.tabNaming.setTabText(self.tabNaming.indexOf(self.tabNameSimple), QtGui.QApplication.translate("MPLayerGui", "Movie (Simple Naming)", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MPLayerGui", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MPLayerGui", "Exit", None, QtGui.QApplication.UnicodeUTF8))

from customqt import UrlEdit

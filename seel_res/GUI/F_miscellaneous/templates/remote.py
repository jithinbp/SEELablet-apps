# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'remote.ui'
#
# Created: Sat Jun  4 19:12:42 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(822, 495)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame_2 = QtGui.QFrame(self.frame)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(-1, 2, 2, 2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pubEdit = QtGui.QLineEdit(self.frame_2)
        self.pubEdit.setText(_fromUtf8(""))
        self.pubEdit.setObjectName(_fromUtf8("pubEdit"))
        self.gridLayout.addWidget(self.pubEdit, 0, 0, 1, 1)
        self.channelLabel = QtGui.QLabel(self.frame_2)
        self.channelLabel.setObjectName(_fromUtf8("channelLabel"))
        self.gridLayout.addWidget(self.channelLabel, 1, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.frame_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.subEdit = QtGui.QLineEdit(self.frame_2)
        self.subEdit.setText(_fromUtf8(""))
        self.subEdit.setObjectName(_fromUtf8("subEdit"))
        self.gridLayout.addWidget(self.subEdit, 0, 1, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(self.frame_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 0, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.results = QtGui.QTextEdit(self.frame_3)
        self.results.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.results.setObjectName(_fromUtf8("results"))
        self.gridLayout_2.addWidget(self.results, 0, 0, 1, 1)
        self.frame_4 = QtGui.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pushButton_3 = QtGui.QPushButton(self.frame_4)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.cmdEdit = QtGui.QLineEdit(self.frame_4)
        self.cmdEdit.setObjectName(_fromUtf8("cmdEdit"))
        self.gridLayout_3.addWidget(self.cmdEdit, 0, 0, 1, 1)
        self.sendID = QtGui.QLineEdit(self.frame_4)
        self.sendID.setMaximumSize(QtCore.QSize(60, 16777215))
        self.sendID.setObjectName(_fromUtf8("sendID"))
        self.gridLayout_3.addWidget(self.sendID, 0, 2, 1, 1)
        self.responseLabel = QtGui.QLabel(self.frame_4)
        self.responseLabel.setObjectName(_fromUtf8("responseLabel"))
        self.gridLayout_3.addWidget(self.responseLabel, 1, 0, 1, 3)
        self.gridLayout_2.addWidget(self.frame_4, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.setListenState)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.execRemote)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.resetKeys)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PubNub based remote access", None))
        self.frame.setProperty("class", _translate("MainWindow", "PeripheralCollection", None))
        self.frame_2.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.pubEdit.setPlaceholderText(_translate("MainWindow", "publish key", None))
        self.channelLabel.setText(_translate("MainWindow", "channel:", None))
        self.checkBox.setText(_translate("MainWindow", "Listen to incoming messages", None))
        self.subEdit.setPlaceholderText(_translate("MainWindow", "subscriber key", None))
        self.pushButton_4.setText(_translate("MainWindow", "Reset keys", None))
        self.frame_3.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.frame_4.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner", None))
        self.pushButton_3.setText(_translate("MainWindow", "Execute on", None))
        self.cmdEdit.setText(_translate("MainWindow", "get_version()", None))
        self.sendID.setText(_translate("MainWindow", "0x02", None))
        self.responseLabel.setText(_translate("MainWindow", "Response:", None))


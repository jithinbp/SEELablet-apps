# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seel_res/GUI/B_ELECTRONICS/A_electronics/templates/ampMod.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 550)
        MainWindow.setMinimumSize(QtCore.QSize(300, 0))
        MainWindow.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../usr/share/pixmaps/cubeview48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setToolTip("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.plot_area_frame = QtWidgets.QFrame(self.splitter)
        self.plot_area_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plot_area_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plot_area_frame.setObjectName("plot_area_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.plot_area_frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.plot_area_frame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 620, 487))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.plot_area = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.plot_area.setContentsMargins(0, 0, 0, 0)
        self.plot_area.setSpacing(0)
        self.plot_area.setObjectName("plot_area")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.frame_4 = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(2, 2, 3, 2)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.frame = QtWidgets.QFrame(self.frame_4)
        self.frame.setMinimumSize(QtCore.QSize(0, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.WidgetLayout = QtWidgets.QHBoxLayout(self.frame)
        self.WidgetLayout.setObjectName("WidgetLayout")
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_11 = QtWidgets.QFrame(self.frame_4)
        self.frame_11.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_11.setMaximumSize(QtCore.QSize(16777215, 115))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.CH1_LABEL = QtWidgets.QLabel(self.frame_11)
        self.CH1_LABEL.setGeometry(QtCore.QRect(20, 10, 51, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.CH1_LABEL.setFont(font)
        self.CH1_LABEL.setObjectName("CH1_LABEL")
        self.CH2_LABEL = QtWidgets.QLabel(self.frame_11)
        self.CH2_LABEL.setGeometry(QtCore.QRect(20, 50, 51, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.CH2_LABEL.setFont(font)
        self.CH2_LABEL.setObjectName("CH2_LABEL")
        self.CH1GainBox = QtWidgets.QComboBox(self.frame_11)
        self.CH1GainBox.setGeometry(QtCore.QRect(100, 10, 91, 21))
        self.CH1GainBox.setObjectName("CH1GainBox")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.CH1GainBox.addItem("")
        self.label_30 = QtWidgets.QLabel(self.frame_11)
        self.label_30.setGeometry(QtCore.QRect(55, 10, 51, 17))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.frame_11)
        self.label_31.setGeometry(QtCore.QRect(55, 50, 51, 17))
        self.label_31.setObjectName("label_31")
        self.CH1_ENABLE = QtWidgets.QCheckBox(self.frame_11)
        self.CH1_ENABLE.setGeometry(QtCore.QRect(0, 10, 21, 20))
        self.CH1_ENABLE.setText("")
        self.CH1_ENABLE.setChecked(True)
        self.CH1_ENABLE.setObjectName("CH1_ENABLE")
        self.CH2_ENABLE = QtWidgets.QCheckBox(self.frame_11)
        self.CH2_ENABLE.setGeometry(QtCore.QRect(0, 50, 21, 20))
        self.CH2_ENABLE.setText("")
        self.CH2_ENABLE.setObjectName("CH2_ENABLE")
        self.CH2GainBox = QtWidgets.QComboBox(self.frame_11)
        self.CH2GainBox.setGeometry(QtCore.QRect(100, 50, 91, 21))
        self.CH2GainBox.setObjectName("CH2GainBox")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.CH2GainBox.addItem("")
        self.verticalLayout_2.addWidget(self.frame_11)
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(118, 40))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 110))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_49 = QtWidgets.QLabel(self.frame_2)
        self.label_49.setGeometry(QtCore.QRect(5, 5, 66, 19))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_49.setFont(font)
        self.label_49.setObjectName("label_49")
        self.time_label = QtWidgets.QLabel(self.frame_2)
        self.time_label.setGeometry(QtCore.QRect(0, 86, 116, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.time_label.setFont(font)
        self.time_label.setText("")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.dial = QtWidgets.QDial(self.frame_2)
        self.dial.setGeometry(QtCore.QRect(20, 10, 81, 91))
        self.dial.setMaximum(9)
        self.dial.setPageStep(1)
        self.dial.setObjectName("dial")
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.trigger_frame = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trigger_frame.sizePolicy().hasHeightForWidth())
        self.trigger_frame.setSizePolicy(sizePolicy)
        self.trigger_frame.setMinimumSize(QtCore.QSize(150, 110))
        self.trigger_frame.setMaximumSize(QtCore.QSize(16777215, 110))
        self.trigger_frame.setStyleSheet("QFrame{background-color: rgba(0, 175, 0, 50);}")
        self.trigger_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.trigger_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trigger_frame.setObjectName("trigger_frame")
        self.trigger_level_label = QtWidgets.QLabel(self.trigger_frame)
        self.trigger_level_label.setGeometry(QtCore.QRect(0, 85, 171, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.trigger_level_label.setFont(font)
        self.trigger_level_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger_level_label.setObjectName("trigger_level_label")
        self.dial_11 = QtWidgets.QDial(self.trigger_frame)
        self.dial_11.setGeometry(QtCore.QRect(85, 10, 91, 81))
        self.dial_11.setMinimum(0)
        self.dial_11.setMaximum(1000)
        self.dial_11.setProperty("value", 500)
        self.dial_11.setNotchTarget(10.0)
        self.dial_11.setNotchesVisible(False)
        self.dial_11.setObjectName("dial_11")
        self.label_4 = QtWidgets.QLabel(self.trigger_frame)
        self.label_4.setGeometry(QtCore.QRect(0, 25, 86, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.trigger_select_box = QtWidgets.QComboBox(self.trigger_frame)
        self.trigger_select_box.setGeometry(QtCore.QRect(0, 50, 86, 27))
        self.trigger_select_box.setStyleSheet("")
        self.trigger_select_box.setIconSize(QtCore.QSize(0, 0))
        self.trigger_select_box.setFrame(True)
        self.trigger_select_box.setObjectName("trigger_select_box")
        self.trigger_select_box.addItem("")
        self.trigger_select_box.addItem("")
        self.triggerBox = QtWidgets.QCheckBox(self.trigger_frame)
        self.triggerBox.setGeometry(QtCore.QRect(0, 0, 101, 24))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.triggerBox.setFont(font)
        self.triggerBox.setChecked(True)
        self.triggerBox.setObjectName("triggerBox")
        self.trigger_level_label.raise_()
        self.label_4.raise_()
        self.trigger_select_box.raise_()
        self.triggerBox.raise_()
        self.dial_11.raise_()
        self.horizontalLayout_2.addWidget(self.trigger_frame)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_6.setStyleSheet("")
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.fit_select_box = QtWidgets.QComboBox(self.frame_6)
        self.fit_select_box.setGeometry(QtCore.QRect(85, 5, 66, 21))
        self.fit_select_box.setObjectName("fit_select_box")
        self.fit_select_box.addItem("")
        self.fit_select_box.addItem("")
        self.fit_select_box.addItem("")
        self.overlay_fit_button = QtWidgets.QCheckBox(self.frame_6)
        self.overlay_fit_button.setGeometry(QtCore.QRect(215, 5, 76, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.overlay_fit_button.setFont(font)
        self.overlay_fit_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.overlay_fit_button.setAutoFillBackground(False)
        self.overlay_fit_button.setIconSize(QtCore.QSize(0, 0))
        self.overlay_fit_button.setObjectName("overlay_fit_button")
        self.fit_select_box_2 = QtWidgets.QComboBox(self.frame_6)
        self.fit_select_box_2.setGeometry(QtCore.QRect(150, 5, 66, 21))
        self.fit_select_box_2.setObjectName("fit_select_box_2")
        self.fit_select_box_2.addItem("")
        self.fit_select_box_2.addItem("")
        self.fit_select_box_2.addItem("")
        self.fit_type_box = QtWidgets.QComboBox(self.frame_6)
        self.fit_type_box.setGeometry(QtCore.QRect(0, 5, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.fit_type_box.setFont(font)
        self.fit_type_box.setFrame(False)
        self.fit_type_box.setObjectName("fit_type_box")
        self.fit_type_box.addItem("")
        self.verticalLayout_2.addWidget(self.frame_6)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 1)
        self.verticalLayout_2.setStretch(6, 2)
        self.verticalLayout_3.addWidget(self.splitter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_9 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 17))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 34))
        self.frame_9.setBaseSize(QtCore.QSize(0, 0))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message_label.sizePolicy().hasHeightForWidth())
        self.message_label.setSizePolicy(sizePolicy)
        self.message_label.setBaseSize(QtCore.QSize(0, 17))
        self.message_label.setStyleSheet("")
        self.message_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.message_label.setWordWrap(False)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        self.freezeButton = QtWidgets.QCheckBox(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freezeButton.sizePolicy().hasHeightForWidth())
        self.freezeButton.setSizePolicy(sizePolicy)
        self.freezeButton.setMaximumSize(QtCore.QSize(100, 10))
        self.freezeButton.setObjectName("freezeButton")
        self.horizontalLayout.addWidget(self.freezeButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_9)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addWidget(self.frame_9)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 932, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuSaveProfile = QtWidgets.QMenu(self.menuBar)
        self.menuSaveProfile.setObjectName("menuSaveProfile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionSaveProfile = QtWidgets.QAction(MainWindow)
        self.actionSaveProfile.setObjectName("actionSaveProfile")
        self.actionLoadProfile = QtWidgets.QAction(MainWindow)
        self.actionLoadProfile.setObjectName("actionLoadProfile")
        self.menuSaveProfile.addAction(self.actionSaveProfile)
        self.menuSaveProfile.addAction(self.actionLoadProfile)
        self.menuBar.addAction(self.menuSaveProfile.menuAction())

        self.retranslateUi(MainWindow)
        self.fit_select_box.setCurrentIndex(2)
        self.fit_select_box_2.setCurrentIndex(2)
        self.fit_type_box.setCurrentIndex(0)
        self.CH1GainBox.currentIndexChanged['int'].connect(MainWindow.setGainCH1)
        self.CH2GainBox.currentIndexChanged['int'].connect(MainWindow.setGainCH2)
        self.dial.valueChanged['int'].connect(MainWindow.setTimeBase)
        self.trigger_select_box.currentIndexChanged['int'].connect(MainWindow.setTriggerChannel)
        self.dial_11.valueChanged['int'].connect(MainWindow.setTriggerLevel)
        self.actionLoadProfile.triggered.connect(MainWindow.loadPro)
        self.actionSaveProfile.triggered.connect(MainWindow.savePro)
        self.pushButton_3.clicked.connect(MainWindow.saveFft)
        self.pushButton_2.clicked.connect(MainWindow.saveData)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Amplitude Modulation"))
        self.centralwidget.setProperty("class", _translate("MainWindow", "PeripheralCollection"))
        self.frame_4.setProperty("class", _translate("MainWindow", "PeripheralCollection"))
        self.label_3.setText(_translate("MainWindow", "Channel Parameters"))
        self.frame_11.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner"))
        self.CH1_LABEL.setText(_translate("MainWindow", "CH1"))
        self.CH2_LABEL.setText(_translate("MainWindow", "CH2"))
        self.CH1GainBox.setItemText(0, _translate("MainWindow", "+/-16V"))
        self.CH1GainBox.setItemText(1, _translate("MainWindow", "+/-8V"))
        self.CH1GainBox.setItemText(2, _translate("MainWindow", "+/-4V"))
        self.CH1GainBox.setItemText(3, _translate("MainWindow", "+/-3V"))
        self.CH1GainBox.setItemText(4, _translate("MainWindow", "+/-2V"))
        self.CH1GainBox.setItemText(5, _translate("MainWindow", "+/-1.5V"))
        self.CH1GainBox.setItemText(6, _translate("MainWindow", "+/-1V"))
        self.CH1GainBox.setItemText(7, _translate("MainWindow", "+/-500mV"))
        self.label_30.setText(_translate("MainWindow", "Range"))
        self.label_31.setText(_translate("MainWindow", "Range"))
        self.CH2GainBox.setItemText(0, _translate("MainWindow", "+/-16V"))
        self.CH2GainBox.setItemText(1, _translate("MainWindow", "+/-8V"))
        self.CH2GainBox.setItemText(2, _translate("MainWindow", "+/-4V"))
        self.CH2GainBox.setItemText(3, _translate("MainWindow", "+/-3V"))
        self.CH2GainBox.setItemText(4, _translate("MainWindow", "+/-2V"))
        self.CH2GainBox.setItemText(5, _translate("MainWindow", "+/-1.5V"))
        self.CH2GainBox.setItemText(6, _translate("MainWindow", "+/-1V"))
        self.CH2GainBox.setItemText(7, _translate("MainWindow", "+/-500mV"))
        self.frame_2.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner"))
        self.label_49.setText(_translate("MainWindow", "TIMEBASE"))
        self.trigger_frame.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner"))
        self.trigger_level_label.setText(_translate("MainWindow", "Level : 0 mV"))
        self.dial_11.setToolTip(_translate("MainWindow", "Scroll to change trigger level"))
        self.label_4.setText(_translate("MainWindow", "Source"))
        self.trigger_select_box.setItemText(0, _translate("MainWindow", "CH1"))
        self.trigger_select_box.setItemText(1, _translate("MainWindow", "CH2"))
        self.triggerBox.setText(_translate("MainWindow", "TRIGGER"))
        self.label_2.setText(_translate("MainWindow", "Data Analysis"))
        self.frame_6.setProperty("class", _translate("MainWindow", "PeripheralCollectionInner"))
        self.fit_select_box.setItemText(0, _translate("MainWindow", "CH1"))
        self.fit_select_box.setItemText(1, _translate("MainWindow", "CH2"))
        self.fit_select_box.setItemText(2, _translate("MainWindow", "None"))
        self.overlay_fit_button.setText(_translate("MainWindow", "Overlay"))
        self.fit_select_box_2.setItemText(0, _translate("MainWindow", "CH1"))
        self.fit_select_box_2.setItemText(1, _translate("MainWindow", "CH2"))
        self.fit_select_box_2.setItemText(2, _translate("MainWindow", "None"))
        self.fit_type_box.setItemText(0, _translate("MainWindow", "SINE FIT"))
        self.message_label.setText(_translate("MainWindow", "Msg:"))
        self.freezeButton.setText(_translate("MainWindow", "FREEZE"))
        self.pushButton_2.setText(_translate("MainWindow", "Save Raw Plots"))
        self.pushButton_3.setText(_translate("MainWindow", "Save FFt"))
        self.menuSaveProfile.setTitle(_translate("MainWindow", "Profiles"))
        self.actionSaveProfile.setText(_translate("MainWindow", "saveProfile"))
        self.actionLoadProfile.setText(_translate("MainWindow", "LoadProfile"))
        self.actionLoadProfile.setShortcut(_translate("MainWindow", "Ctrl+O"))

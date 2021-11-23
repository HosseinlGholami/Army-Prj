# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlaybackUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(830, 521)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(830, 500))
        MainWindow.setMaximumSize(QtCore.QSize(830, 521))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(830, 500))
        self.centralwidget.setMaximumSize(QtCore.QSize(830, 500))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 164, 481))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.RefreshButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.RefreshButton.setObjectName("RefreshButton")
        self.verticalLayout_5.addWidget(self.RefreshButton)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.ServerListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.ServerListWidget.setObjectName("ServerListWidget")
        self.verticalLayout_3.addWidget(self.ServerListWidget)
        self.add_jobButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.add_jobButton.setObjectName("add_jobButton")
        self.verticalLayout_3.addWidget(self.add_jobButton)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.JobListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.JobListWidget.setObjectName("JobListWidget")
        self.verticalLayout_4.addWidget(self.JobListWidget)
        self.remove_jobButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.remove_jobButton.setObjectName("remove_jobButton")
        self.verticalLayout_4.addWidget(self.remove_jobButton)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.AvailListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget_3)
        self.AvailListWidget.setObjectName("AvailListWidget")
        self.verticalLayout_5.addWidget(self.AvailListWidget)
        self.playButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.playButton.setObjectName("playButton")
        self.verticalLayout_5.addWidget(self.playButton)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(180, 10, 640, 480))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.RefreshButton.setText(_translate("MainWindow", "refresh"))
        self.label.setText(_translate("MainWindow", "Server List"))
        self.add_jobButton.setText(_translate("MainWindow", "-->"))
        self.label_2.setText(_translate("MainWindow", "Job List"))
        self.remove_jobButton.setText(_translate("MainWindow", "<--"))
        self.label_3.setText(_translate("MainWindow", "avail List"))
        self.playButton.setText(_translate("MainWindow", "play"))
        self.label_4.setText(_translate("MainWindow", "None"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

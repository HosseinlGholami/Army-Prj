# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginServerUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(300, 480))
        MainWindow.setMaximumSize(QtCore.QSize(300, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 31))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 40, 261, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 51, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 160, 51, 16))
        self.label_4.setObjectName("label_4")
        self.LogtextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.LogtextBrowser.setGeometry(QtCore.QRect(10, 300, 271, 131))
        self.LogtextBrowser.setObjectName("LogtextBrowser")
        self.Username_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Username_lineEdit.setGeometry(QtCore.QRect(90, 130, 181, 20))
        self.Username_lineEdit.setObjectName("Username_lineEdit")
        self.Password_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Password_lineEdit.setGeometry(QtCore.QRect(90, 160, 181, 20))
        self.Password_lineEdit.setObjectName("Password_lineEdit")
        self.login_Button = QtWidgets.QPushButton(self.centralwidget)
        self.login_Button.setGeometry(QtCore.QRect(140, 210, 131, 41))
        self.login_Button.setObjectName("login_Button")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.label_5.setObjectName("label_5")
        self.Username_lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.Username_lineEdit_2.setGeometry(QtCore.QRect(90, 70, 181, 20))
        self.Username_lineEdit_2.setObjectName("Username_lineEdit_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 100, 61, 16))
        self.label_6.setObjectName("label_6")
        self.Username_lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.Username_lineEdit_3.setGeometry(QtCore.QRect(90, 100, 181, 20))
        self.Username_lineEdit_3.setObjectName("Username_lineEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to Processing Server applicatoin"))
        self.label_3.setText(_translate("MainWindow", "Username"))
        self.label_4.setText(_translate("MainWindow", "Password"))
        self.Username_lineEdit.setText(_translate("MainWindow", "guest"))
        self.Password_lineEdit.setText(_translate("MainWindow", "guest"))
        self.login_Button.setText(_translate("MainWindow", "Login"))
        self.label_5.setText(_translate("MainWindow", "Server address"))
        self.Username_lineEdit_2.setText(_translate("MainWindow", "localhost"))
        self.label_6.setText(_translate("MainWindow", "Server port"))
        self.Username_lineEdit_3.setText(_translate("MainWindow", "5672"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QProcess
from ReceiveUI import Ui_MainWindow
import pika


QUEUE= sys.argv[1]
blF=int(sys.argv[2])
rF =int(sys.argv[3])
gF =int(sys.argv[4])
bF =int(sys.argv[5])


class RunDesignerGUI():
    def __init__(self):
        self.Data=dict()

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # self.widget_action()
        
        self.MainWindow.show()
        sys.exit(app.exec_())
    
    # def widget_action(self):
    #     self.ui.actionClose.setStatusTip("Exit the application")
    #     self.ui.actionClose.triggered.connect(self.close_GUI)
    #     self.ui.addc_Button.clicked.connect(self.add_camera)
              


if __name__ == "__main__":
    RunDesignerGUI(blF,rF,gF,bF)
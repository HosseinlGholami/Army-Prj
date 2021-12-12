import sys
from PyQt5 import QtWidgets
from ServerUI import Ui_MainWindow

class RunDesignerGUI():
    def __init__(self):
        self.Data=dict()
        self.DmData=dict()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.widget_action()
        self.update_widgets()
        
        # self.send_log(str(self.Data))
        # self.send_log(str(self.DmData))

        self.MainWindow.show()
        sys.exit(app.exec_())
    #import related function 
    from util import  add_camera,delete_camera,start_send_cam_data,stop_send_cam_data,restore_last_config,login
    
    def widget_action(self):
        self.ui.actionClose.setStatusTip("Exit the application")
        self.ui.actionClose.triggered.connect(self.close_GUI)
        #login
        self.ui.Login_Button.clicked.connect(self.login)
        #add camera
        self.ui.addc_Button.clicked.connect(self.add_camera)
        #send button
        self.ui.StrSenButton.clicked.connect(self.start_send_cam_data)
        self.ui.StpSenButton.clicked.connect(self.stop_send_cam_data)
        #delete camera
        self.ui.StpSenButton.clicked.connect(self.stop_send_cam_data)
        self.ui.delete_cam_Button.clicked.connect(self.delete_camera)

    def send_log(self,txt):
        pre_txt=self.ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.ui.LogtextBrowser.setText(txt)
        else:
            self.ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
    def close_GUI(self):
        self.MainWindow.close()
        
    def update_widgets(self):
        for i in range(1,4):
            self.ui.tabWidget.setTabVisible(i,False)
        self.MainWindow.setWindowTitle("JANGAL")
            

if __name__ == "__main__":
    RunDesignerGUI()    
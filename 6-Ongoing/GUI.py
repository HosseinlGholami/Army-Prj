import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QProcess
from UI import Ui_MainWindow
import pika



class RunDesignerGUI():
    def __init__(self):
        self.Data=dict()

        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.widget_action()
        self.update_widgets()

        self.MainWindow.show()
        sys.exit(app.exec_())
    
    def widget_action(self):
        self.ui.actionClose.setStatusTip("Exit the application")
        self.ui.actionClose.triggered.connect(self.close_GUI)
        self.ui.addc_Button.clicked.connect(self.add_camera)
        self.ui.ShowButton.clicked.connect(self.show_camera)

    def add_camera(self):
        CAMERA_IP=self.ui.CIplineEdit.text()
        CAMERA_NAME=self.ui.CNamelineEdit.text()
        #add to combo box
        self.ui.CamNameComboBox.addItem(CAMERA_NAME)
        #save the file as dict
        self.Data.update({CAMERA_NAME:[CAMERA_IP, QProcess() , QProcess() ]})
        
        #connect to server and create Queue
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost',
                                                5672,
                                                '/',
                                                credentials)
        channel=pika.BlockingConnection(parameters).channel()
        channel.queue_declare(queue=CAMERA_NAME)
        channel.queue_bind(exchange='e.R',
                    queue=CAMERA_NAME)
        
        
        self.send_log("Queue has created")
        
    
    def show_camera(self):
        CAMERA_NAME = self.ui.CamNameComboBox.currentText()
        CAMERA_IP=self.Data[CAMERA_NAME][0]
                
        #connect reciever to server
        pr=self.Data[CAMERA_NAME][1]
        pr.start("python",["Receive.py",CAMERA_NAME])
        self.send_log("Receiver connect to queue")
        #the camera send data to server
        ps=self.Data[CAMERA_NAME][2]
        ps.start("python",["Sender.py",CAMERA_NAME,CAMERA_IP])
        self.send_log("Sender Send Data to queue")
        

    def send_log(self,txt):
        pre_txt=self.ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.ui.LogtextBrowser.setText(txt)
        else:
            self.ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
    def close_GUI(self):
        self.MainWindow.close()
    def update_widgets(self):
        self.MainWindow.setWindowTitle("JANGAL")
            
        


if __name__ == "__main__":
    RunDesignerGUI()    
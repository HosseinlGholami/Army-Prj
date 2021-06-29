import sys
from PyQt5 import QtWidgets
from ClientUI import Ui_MainWindow
import requests, json
from PyQt5.QtCore import QProcess

def call_rabbitmq_api_validation(host, port, user, passwd):
  url = 'http://%s:%s/api/whoami' % (host, port)
  r = requests.get(url, auth=(user,passwd))
  return dict(r.json())
def get_active_exchange(host, port, user, passwd):
    a=list()
    GET_VHOST = f"http://{host}:{port}/api/definitions"
    r = requests.get(url = GET_VHOST ,auth=(user, passwd),)
    return [ex['name'] for ex in dict(r.json())['exchanges']]
def get_server_param():
    with open('Server.inf') as reader:
        return {x.split('=')[0]:x.split('=')[1] for x in reader.read().split('\n')}

class RunDesignerGUI():
    def __init__(self):
        self.process=list()
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.first_veiw=[self.ui.Login_Button,self.ui.Username_lineEdit,self.ui.Password_lineEdit,self.ui.label_3,self.ui.label_4]
        self.second_veiw=[self.ui.Show_Button,self.ui.CamNameComboBox,self.ui.label_10,self.ui.Logout_Button]
        self.veiwing=self.first_veiw+self.second_veiw
        self.widget_action()
        self.update_widgets()

        self.MainWindow.show()
        sys.exit(app.exec_())

 
    def widget_action(self):
        self.ui.Login_Button.clicked.connect(self.login_function)
        self.ui.Show_Button.clicked.connect(self.showcam_function)
        self.ui.Logout_Button.clicked.connect(self.logout_function)
    def showcam_function(self):
        username=self.ui.Username_lineEdit.text()
        password=self.ui.Password_lineEdit.text()
        exchange_name=self.ui.CamNameComboBox.currentText()
        self.process.append(QProcess())
        self.process[-1].finished.connect(self.finish_process)
        self.process[-1].start("python",["Receiver.py",username,password,exchange_name])
    
    def finish_process(self,  exitCode,  exitStatus):
        for i,item in enumerate(self.process):
            if item.state() ==0:
                del self.process[i]
            
        self.send_log('number of the active camera'+str(len(self.process)))
        
    def logout_function(self):
        self.change_veiw(self.veiwing)
        self.send_log('back to login page')
        
    def login_function(self):
        #should be read from file
        serverparam=get_server_param()
        serverip=serverparam['serverip']
        serverport=serverparam['port']
        username=self.ui.Username_lineEdit.text()
        password=self.ui.Password_lineEdit.text()
        try:
            rabbit_authoriation=call_rabbitmq_api_validation(serverip,serverport,username,password)
        except:
            self.send_log("server is down")
            rabbit_authoriation={'error':'offline'}
        if 'name' in rabbit_authoriation:
                #login code is here !
                self.change_veiw(self.veiwing)
                self.send_log('login successful')
                for exchange_name in get_active_exchange(serverip,serverport,username,password):
                    self.ui.CamNameComboBox.addItem(exchange_name)
        else:
            flag=False
            self.send_log(f"rabbit_authoriation failed: error --> {rabbit_authoriation['error']}")
        
    def change_veiw(self,items):
        for item in items:
            item.setHidden(not item.isHidden())
    def send_log(self,txt):
        pre_txt=self.ui.LogtextBrowser.toPlainText()
        if (pre_txt==''):
            self.ui.LogtextBrowser.setText(txt)
        else:
            self.ui.LogtextBrowser.setText(pre_txt+'\n'+txt)
    def close_GUI(self):
        self.MainWindow.close()
    def update_widgets(self):
        self.change_veiw(self.second_veiw)
        self.MainWindow.setWindowTitle("JANGAL-Client")
            

if __name__ == "__main__":
    RunDesignerGUI()    
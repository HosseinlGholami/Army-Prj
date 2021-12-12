import sys
from PyQt5 import QtWidgets
from ui import  Ui_MainWindow

class RunDesignerGUI():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.updateWidget()
        self.widgetsAction()
        
        self.MainWindow.show()
        sys.exit(app.exec_())
    
    def updateWidget(self):
        self.MainWindow.setWindowTitle('Va alekom ASALAM')
        self.ui.label.setText('Va alekom ASALAM')
    
    def widgetsAction(self):
        self.ui.actionExit.triggered.connect(self.close_GUI)
        self.ui.actionExit.setShortcut("Ctrl+Q")
        
    
    def close_GUI(self):
        self.MainWindow.close()
        
if __name__ == "__main__":
    RunDesignerGUI()    
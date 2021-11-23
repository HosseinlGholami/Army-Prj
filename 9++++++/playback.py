import sys
from PyQt5 import QtWidgets
from ui.PlaybackUI import Ui_MainWindow
from minio import Minio
import time

CAM_NAME="c1"
MINIO_SERVER_ADDR='localhost:9000'
MINIO_USER_FROM_DOCKER_FILE='admin'
MINIO_PASS_FROM_DOCKER_FILE='admin1234'

class RunDesignerGUI():
    def __init__(self):
        self.minioClient = Minio(MINIO_SERVER_ADDR, access_key=MINIO_USER_FROM_DOCKER_FILE, secret_key=MINIO_PASS_FROM_DOCKER_FILE, secure=False)
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.widget_action()
        
        self.MainWindow.show()
        sys.exit(app.exec_())

    def widget_action(self):
        #list_select_update
        self.ui.ServerListWidget.itemSelectionChanged.connect(self.server_list_selected_change)
        self.ui.JobListWidget.itemSelectionChanged.connect(self.job_list_selected_change)
        self.ui.AvailListWidget.itemSelectionChanged.connect(self.avail_list_selected_change)
        
        #add job butten
        self.ui.add_jobButton.clicked.connect(self.add_job)
        self.ui.remove_jobButton.clicked.connect(self.remove_job)
        
        #refresh
        self.ui.RefreshButton.clicked.connect(self.do_refresh)
        
        self.ui.playButton.clicked.connect(self.run_the_play_therad)
        
        
        self.do_refresh()
    def run_the_play_therad():
        print("hala video ham neshoon midam")
        pass
    
    def remove_job(self):
        #TODO: 
            #remove the selected chunk 
            #remove from the avail
        pass
    
    def add_job(self):
        #TODO:
            #download the selected chuck
            #add that chunk inside the avail
        pass    
    
    def do_refresh(self):
        self.ui.ServerListWidget.clear()
        buckets = self.minioClient.list_buckets()
        minio_buckets=[buckets.name.split('jangal_ex_')[1] for buckets in buckets]
        if CAM_NAME in minio_buckets:
            bucket_index=minio_buckets.index(CAM_NAME)
            objects = self.minioClient.list_objects(buckets[bucket_index].name, 
                                          recursive=True)
            minio_objects=[obj.object_name for obj in objects]
            self.minio_dict={self.object_name_convertor(x):x for x in minio_objects}
        self.ui.ServerListWidget.addItems([keys for keys in self.minio_dict])
        
    def object_name_convertor(self,file_name):
        string_time=file_name.split('.')[0]
        return time.strftime(" %H:%M-%a", time.gmtime(int(string_time)))
                                 
    def server_list_selected_change(self):
        server_selected_set=self.ui.ServerListWidget.selectedItems()
        item=[item.text() for item in server_selected_set][0]
        self.server_selected=self.minio_dict[item]
        
    def job_list_selected_change(self):
        job_selected_set=self.ui.JobListWidget.selectedItems()
        item=[item.text() for item in job_selected_set][0]
        self.job_selected=self.minio_dict[item]
        
    def avail_list_selected_change(self):
        avail_selected_set=self.ui.AvailListWidget.selectedItems()
        item=[item.text() for item in avail_selected_set][0]
        self.avail_selected=self.minio_dict[item]
        
if __name__ == "__main__":
    RunDesignerGUI()    
import sys
from PyQt5 import QtWidgets,QtGui
from threading import Thread
from multiprocessing import Queue
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QPixmap
from ui.PlaybackUI import Ui_MainWindow
import numpy as np
import os
import cv2 as cv
from minio import Minio
import time

CAM_NAME=sys.argv[1]
MINIO_SERVER_ADDR=sys.argv[2]
MINIO_USER=sys.argv[3]
MINIO_PASS=sys.argv[4]

# CAM_NAME="c1"
# MINIO_SERVER_ADDR='localhost:9000'
# MINIO_USER='admin'
# MINIO_PASS='admin1234'


DOWNLOAD_PATH=f"./download/{CAM_NAME}"

class video_Signals(QWidget):
    change_pixmap_signal = pyqtSignal(np.ndarray)

class video_player_thread(QThread):
    def __init__(self,Name,Signal):
        super(video_player_thread, self).__init__()
        self.signal=Signal
        self.video_name=Name
    def run(self):
        print(DOWNLOAD_PATH+"/"+self.video_name)
        self.cap = cv.VideoCapture(DOWNLOAD_PATH+"/"+self.video_name)
        while(True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # if frame is read correctly ret is True
            if not ret:
                # print("Can't receive frame (stream end?). Exiting ...")
                self.signal.emit(np.array([]))
                break
            else:
                self.signal.emit(frame)
        self.cap.release()
        
    
class download_Signals(QWidget):
    change_pixmap_signal = pyqtSignal(str)
    
def object_name_convertor(file_name,for_file=False):
    string_time=file_name.split('.')[0]
    if for_file:
        return time.strftime("%H-%M-%D", time.gmtime(int(string_time))).replace("/","_")+".avi"
    else:
        return time.strftime("%H:%M-%D", time.gmtime(int(string_time))).replace("/","_")

def change_name_for_list_from_file(string):
    first_simbol_index=string.find("-")
    return "".join(string[:first_simbol_index]+":"+string[first_simbol_index+1:]).split(".")[0]

BUCKET_NAME="jangal_ex_"+CAM_NAME

class minio_downloader(Thread):
    def __init__(self,reciever_queue,minioclient,Signal):
        Thread.__init__(self)
        self.queue=reciever_queue
        self.channel=minioclient
        self.signal=Signal
    def run(self):
        while(True):
            file_name=self.queue.get(block=True)
            print(file_name)
            data = self.channel.get_object(BUCKET_NAME,file_name)
            with open(DOWNLOAD_PATH+"/"+object_name_convertor(file_name,True), 'wb') as file_data:
                for d in data.stream(1000*1024*1024):
                    file_data.write(d)
            self.signal.emit(object_name_convertor(file_name))
class RunDesignerGUI():
    def __init__(self):
        self.minioClient = Minio(MINIO_SERVER_ADDR, access_key=MINIO_USER, secret_key=MINIO_PASS, secure=False)
        app = QtWidgets.QApplication(sys.argv)
        app.aboutToQuit.connect(self.closeEvent)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.active_video=False
        self.received_video_signal=video_Signals()
        self.download_queue=Queue()
        self.download_done_signal=download_Signals()
        minio_downloader_handel=minio_downloader(self.download_queue,self.minioClient,self.download_done_signal.change_pixmap_signal)
        minio_downloader_handel.start()
        
        self.widget_action()
        
        
        self.MainWindow.show()
        sys.exit(app.exec_())

    def widget_action(self):
        #list_select_update
        self.ui.ServerListWidget.itemSelectionChanged.connect(self.server_list_selected_change)
        self.ui.AvailListWidget.itemSelectionChanged.connect(self.avail_list_selected_change)
        
        #add job butten
        self.ui.download_Button.clicked.connect(self.download_job)
        self.download_done_signal.change_pixmap_signal.connect(self.get_done_downloaded_signal)
        self.ui.remove_Button.clicked.connect(self.remove_job)
        
        #refresh
        self.ui.RefreshButton.clicked.connect(self.do_refresh)
        #play video
        self.ui.playButton.clicked.connect(self.run_the_play_therad)
        self.received_video_signal.change_pixmap_signal.connect(self.update_image)

        
        self.do_refresh()
        #reload what it has download befor for camera if somethings existed
        if CAM_NAME in os.listdir("download"):
            list_of_available_downloaded_file=[change_name_for_list_from_file(x) for x in os.listdir(DOWNLOAD_PATH)]
        else:
            list_of_available_downloaded_file=[]
            os.mkdir(DOWNLOAD_PATH)
        self.ui.AvailListWidget.addItems(list_of_available_downloaded_file)
        self.avail_list=list_of_available_downloaded_file
        
    def run_the_play_therad(self):
        if self.active_video:
            self.video_player.terminate()
            self.active_video=False
        self.video_player=video_player_thread(self.avail_selected,self.received_video_signal.change_pixmap_signal)
        self.video_player.setTerminationEnabled()
        self.video_player.start()
        self.active_video=True
        
    
    def remove_job(self):
        #remove from qlist
        listItems=self.ui.AvailListWidget.selectedItems()
        if not listItems: return        
        for item in listItems:
           self.ui.AvailListWidget.takeItem(self.ui.AvailListWidget.row(item))
        
        #remove from local
        # print("remove:"+self.avail_selected)
        os.remove(DOWNLOAD_PATH+"/"+self.avail_selected)
        
    def download_job(self):
        self.download_queue.put(self.server_selected)
    def get_done_downloaded_signal(self,file_name):
        if not file_name in self.avail_list:
            self.avail_list.append(file_name)
            self.ui.AvailListWidget.addItems([file_name])
        
        
    def do_refresh(self):
        self.ui.ServerListWidget.clear()
        buckets = self.minioClient.list_buckets()
        minio_buckets=[buckets.name.split('jangal_ex_')[1] for buckets in buckets]
        if CAM_NAME in minio_buckets:
            bucket_index=minio_buckets.index(CAM_NAME)
            objects = self.minioClient.list_objects(buckets[bucket_index].name, 
                                          recursive=True)
            minio_objects=[obj.object_name for obj in objects]
            self.minio_dict={object_name_convertor(x):x for x in minio_objects}
        self.ui.ServerListWidget.addItems([keys for keys in self.minio_dict])
        
    def server_list_selected_change(self):
        server_selected_set=self.ui.ServerListWidget.selectedItems()
        item=[item.text() for item in server_selected_set][0]
        self.server_selected=self.minio_dict[item]
        
        
    def avail_list_selected_change(self):
        avail_selected_set=self.ui.AvailListWidget.selectedItems()
        if not avail_selected_set: return        
        item=[item.text() for item in avail_selected_set][0]
        self.avail_selected=object_name_convertor(self.minio_dict[item],True)
    
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if len(cv_img):
            qt_img = self.convert_cv_qt(cv_img)
            self.ui.image_label.setPixmap(qt_img)
        else:
            self.active_video=False
        
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.ui.image_label.width(), self.ui.image_label.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def closeEvent(self):
        del self.minioClient
        self.MainWindow.close()
        self.video_player.terminate()
        raise Exception('close', 'playback')
        

if __name__ == "__main__":
    RunDesignerGUI()    
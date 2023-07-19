'''
Flame AVSim S/W Manager Application
@author Byunghun Hwang<bh.hwang@iae.re.kr>
'''

import sys, os
import typing
from PyQt6 import QtGui
import pathlib
import json
from PyQt6.QtGui import QImage, QPixmap, QCloseEvent, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QLabel, QPushButton, QMessageBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import QObject, Qt, QTimer, QThread, pyqtSignal, pyqtSlot
import timeit
import paho.mqtt.client as mqtt
from datetime import datetime
import csv
import math

WORKING_PATH = pathlib.Path(__file__).parent
APP_UI = WORKING_PATH / "MainWindow.ui"

'''
scenario execution thread
'''
class ScenarioRunner(QTimer):
    do_act_scenario = pyqtSignal(float, str, str) #time key, mapi, message

    def __init__(self, interval):
        super().__init__()
        self.time_interval = interval
        self.setInterval(interval) # 100ms interval
        self.timeout.connect(self.run)
        self.current_time_idx = 0   # time begin 0
        self.scenario_container = {}
        
    # scenario running callback
    def run(self):
        start_t = timeit.default_timer()
        
        # post processing
        t_key = round(self.current_time_idx, 1)
        if t_key in self.scenario_container.keys():
            for m in self.scenario_container[t_key]:
                self.do_act_scenario.emit(t_key, m["mapi"], m["message"])
            
        self.current_time_idx += self.time_interval/1000 # update time index
        
        end_t = timeit.default_timer()
    
    def load_scenario(self, json_scenario):
        try:
            if "scenario" in json_scenario:
                for scene in json_scenario["scenario"]:
                    self.scenario_container[scene["time"]] = []
                    for event in scene["event"]:
                        self.scenario_container[scene["time"]].append(event)
            
            # for t in self.scenario_container.keys():
            #     print(self.scenario_container[t], len(self.scenario_container[t]))
            
        except json.JSONDecodeError as e:
            pass
    
    # start timer
    def run_scenario(self):
        print("start running scenario...")
        self.start()
    
    # stop timer
    def stop_scenario(self):
        print("stop running scenario...")
        self.stop()
        
            
    def __str__(self):
        return str(self.camera_id)
    
'''
Main window
'''
class AVSimManager(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(APP_UI, self)

        self.sub_api = {}
        self.columns = ["Index", "Time(s)", "MAPI", "Message"]
        
        # callback function connection for menu
        self.actionOpen.triggered.connect(self.open_scenario_file)
        self.btn_scenario_run.clicked.connect(self.api_run_scenario)
        self.btn_scenario_stop.clicked.connect(self.api_stop_scenario)
        self.btn_scenario_pause.clicked.connect(self.api_pause_scenario)
        self.btn_scenario_resume.clicked.connect(self.api_resume_scenario)
        self.btn_scenario_stepover.clicked.connect(self.api_stepover_scenario)
        
        self.scenario_model = QStandardItemModel()
        self.scenario_model.setColumnCount(len(self.columns))
        self.scenario_model.setHorizontalHeaderLabels(self.columns)
        self.table_scenario_contents.setModel(self.scenario_model)
        
        # for mqtt connection
        self.mq_client = mqtt.Client(client_id="flame-avsim-manager",transport='tcp',protocol=mqtt.MQTTv311, clean_session=True)
        self.mq_client.on_connect = self.on_mqtt_connect
        self.mq_client.on_message = self.on_mqtt_message
        self.mq_client.on_disconnect = self.on_mqtt_disconnect
        self.mq_client.connect_async("127.0.0.1",port=1883,keepalive=60)
        self.mq_client.loop_start()
    
        # runner instance (with time interval value, 100ms)
        self.runner = ScenarioRunner(interval=100)
        self.runner.do_act_scenario.connect(self.do_publish)
    
    def update_scenario(self, data_rows):
        pass
        #for row in data_rows
        # self.scenario_model.appendRow([QStandardItem("1"), QStandardItem("Scenario 1")])
        
        
    def open_scenario_file(self):
        selected_file = QFileDialog.getOpenFileName(self, 'Open scenario file', './')
        if selected_file[0]:
            sfile = open(selected_file[0], "r")
            with sfile:
                try:
                    scenario_json_data = json.load(sfile)
                except Exception as e:
                    QMessageBox.critical(self, "Error", "Scenario file read error {}".format(str(e)))
                    
                # parse scenario file
                self.runner.load_scenario(scenario_json_data)
                self.scenario_model.setRowCount(0)
                if "scenario" in scenario_json_data:
                    for data in scenario_json_data["scenario"]:
                        for event in data["event"]:
                            self.scenario_model.appendRow([QStandardItem(str(data["index"])), QStandardItem(str(data["time"])), QStandardItem(event["mapi"]), QStandardItem(event["message"])])
        
                
    # message-based api
    def api_run_scenario(self):
        self.runner.run_scenario()
    
    def api_stop_scenario(self):
        self.runner.stop_scenario()
    
    def api_pause_scenario(self):
        pass
    
    def api_resume_scenario(self):
        pass
    
    def api_stepover_scenario(self):
        pass
    
    def do_publish(self, time, mapi, message):
        self.mq_client.publish(mapi, message, 0)

                
    # show message on status bar
    def show_on_statusbar(self, text):
        self.statusBar().showMessage(text)
    

    # close event callback function by user
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.api_stop_scenario()

        return super().closeEvent(a0)
    
    # MQTT callbacks
    def on_mqtt_connect(self, mqttc, obj, flags, rc):        
        self.show_on_statusbar("Connected to Broker({})".format(str(rc)))
        
    def on_mqtt_disconnect(self, mqttc, userdata, rc):
        pass
        
    def on_mqtt_message(self, mqttc, userdata, msg):
        pass
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AVSimManager()
    window.show()
    sys.exit(app.exec())
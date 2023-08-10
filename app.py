'''
Flame AVSim S/W Manager Application
@author Byunghun Hwang<bh.hwang@iae.re.kr>
'''

import sys, os
import typing
from PyQt6 import QtGui
import pathlib
import json
from PyQt6.QtGui import QImage, QPixmap, QCloseEvent, QStandardItem, QStandardItemModel, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QLabel, QPushButton, QMessageBox
from PyQt6.QtWidgets import QFileDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import QModelIndex, QObject, Qt, QTimer, QThread, pyqtSignal, QAbstractTableModel
import timeit
import paho.mqtt.client as mqtt
from datetime import datetime
import csv
import math

WORKING_PATH = pathlib.Path(__file__).parent # working path
APP_UI = WORKING_PATH / "MainWindow.ui" # Qt-based UI file
APP_NAME = "avsim-manager" # application name

'''
scenario execution thread
'''
class ScenarioRunner(QTimer):

    scenario_act_slot = pyqtSignal(float, str, str) #arguments : time_key, mapi, message

    def __init__(self, interval_ms):
        super().__init__()
        self.time_interval = interval_ms # default interval_ms = 100ms
        self.setInterval(interval_ms)
        self.timeout.connect(self.on_timeout_callback) # timer callback
        self.current_time_idx = 0  # time index
        self.scenario_container = {} # scenario data container
        
    # scenario running callback by timeout event
    def on_timeout_callback(self):
        
        time_key = round(self.current_time_idx, 1)
        if time_key in self.scenario_container.keys():
            for msg in self.scenario_container[time_key]:
                self.scenario_act_slot.emit(time_key, msg["mapi"], msg["message"])
            
        self.current_time_idx += self.time_interval/1000 # update time index
    
    # open & load scenario file
    def load_scenario(self, scenario:dict) -> bool:
        self.stop_scenario() # if timer is running, stop the scenario runner

        if len(scenario)<1:
            print("> Empty Scenario. Please check your scenario")
            return False
        
        try:
            if "scenario" in scenario:
                for scene in scenario["scenario"]:
                    self.scenario_container[scene["time"]] = [] # time indexed container
                    for event in scene["event"]: # for every events
                        self.scenario_container[scene["time"]].append(event) # append event
            
        except json.JSONDecodeError as e:
            print("JSON Decode error", str(e))
    
    # start timer
    def run_scenario(self):
        if self.isActive(): # if the timer is now active(=running)
            self.stop() # stop the timer
        self.start() # then restart the timer
    
    # stop timer
    def stop_scenario(self):
        self.current_time_idx = 0 # timer index set 0
        self.stop() # timer stop
        
    # pause timer
    def pause_scenario(self):
        self.stop() # stop the timer, but timer index does not set 0

'''
Main window
'''
class AVSimManager(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(APP_UI, self)

        # mapi interface function (subscribe the mapi)
        self.message_api = {
            "flame/avsim/mapi_notify_active" : self.mapi_notify_active
            #"flame/avsim/carla/mapi_set_ego_status"
        }
        self.scenario_table_columns = ["Time(s)", "MAPI", "Message"]
        self.coapp_table_columns = ["App", "Active", "Status"]
        
        
        # callback function connection for menu
        self.actionOpen.triggered.connect(self.open_scenario_file)
        self.btn_scenario_run.clicked.connect(self.api_run_scenario)
        self.btn_scenario_stop.clicked.connect(self.api_stop_scenario)
        self.btn_scenario_pause.clicked.connect(self.api_pause_scenario)
        self.btn_scenario_reload.clicked.connect(self.scenario_reload)
        self.btn_scenario_save.clicked.connect(self.scenario_save)
        
        # scenario model for scenario table
        self.scenario_model = QStandardItemModel()
        self.scenario_model.setColumnCount(len(self.scenario_table_columns))
        self.scenario_model.setHorizontalHeaderLabels(self.scenario_table_columns)
        self.table_scenario_contents.setModel(self.scenario_model)

        
        # status model for coapp table
        self.coapp_model = QStandardItemModel()
        self.coapp_model.setColumnCount(len(self.coapp_table_columns))
        self.coapp_model.setHorizontalHeaderLabels(self.coapp_table_columns)
        self.table_coapp_status.setModel(self.coapp_model)
        coapps = ["avsim-cam", "avsim-cdlink", "avsim-neon", "avsim-carla"]
        for app in coapps:
            self.coapp_model.appendRow([QStandardItem(app), QStandardItem("-"), QStandardItem("-")])
            #self.coapp_model.appendRow([QStandardItem(app).setTextAlignment(Qt.AlignmentFlag.AlignCenter), QStandardItem("-"), QStandardItem("-")])
        
        
        # for mqtt connection
        self.mq_client = mqtt.Client(client_id="flame-avsim-manager",transport='tcp',protocol=mqtt.MQTTv311, clean_session=True)
        self.mq_client.on_connect = self.on_mqtt_connect
        self.mq_client.on_message = self.on_mqtt_message
        self.mq_client.on_disconnect = self.on_mqtt_disconnect
        self.mq_client.connect_async("127.0.0.1",port=1883,keepalive=60)
        self.mq_client.loop_start()
    
        # runner instance (with time interval value, 100ms)
        self.runner = ScenarioRunner(interval_ms=100)
        self.runner.scenario_act_slot.connect(self.do_publish)
        
    
    # open & load scenario file    
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
                            self.scenario_model.appendRow([QStandardItem(str(data["time"])), QStandardItem(event["mapi"]), QStandardItem(event["message"])])

                # table view column width resizing
                self.table_scenario_contents.resizeColumnsToContents()
            
    # change row background color
    def _mark_row_color(self, row):
        for col in range(self.scenario_model.columnCount()):
            self.scenario_model.item(row,col).setBackground(QColor(255,0,0,100))
    
    # reset all rows background color
    def _mark_row_reset(self):
        for col in range(self.scenario_model.columnCount()):
            for row in range(self.scenario_model.rowCount()):
                self.scenario_model.item(row,col).setBackground(QColor(0,0,0,0))
    
    # scenario reload
    def scenario_reload(self):
        pass
        
    def scenario_save(self):
        pass
                
    # message-based api
    def api_run_scenario(self):
        self.runner.run_scenario()
        self.show_on_statusbar("Start scenario running...")
    
    def api_stop_scenario(self):
        self.runner.stop_scenario()
        self.show_on_statusbar("Stopped scenario running...")
    
    def api_pause_scenario(self):
        self.runner.pause_scenario()
    
    def do_publish(self, time, mapi, message):
        self.mq_client.publish(mapi, message, 0)
        
        self._mark_row_reset()
        for row in range(self.scenario_model.rowCount()):
            if time == float(self.scenario_model.item(row, 1).text()):
                self._mark_row_color(row)
    
    def api_notify_active(self, payload):
        if type(payload)!= dict:
            print("error : payload must be dictionary type")
            return
        
        app_key = "app"
        active_key = "active"
        if active_key in payload.keys():
            active_value = payload[active_key] # boolean
            # find row
            for row in range(self.coapp_model.rowCount()):
                print(type(self.coapp_model.index(row, 0).data()))
                if self.coapp_model.index(row, 0).data() == payload[app_key]:
                    # update item data
                    self.coapp_model.setData(self.coapp_model.index(row, 1), payload[active_key])
                    break
            
        
    
    def mapi_notify_active(self):
        if self.mq_client.is_connected():
            msg = {"app":"avsim-manager", "active":True}
            self.mq_client.publish("flame/avsim/notify_active", json.dumps(msg), 0)
        
                
    # show message on status bar
    def show_on_statusbar(self, text):
        self.statusBar().showMessage(text)
    

    # close event callback function by user
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.api_stop_scenario()

        return super().closeEvent(a0)
    
    # MQTT callbacks
    def on_mqtt_connect(self, mqttc, obj, flags, rc):
        # subscribe message api
        for topic in self.message_api.keys():
            self.mq_client.subscribe(topic, 0)
        
        self.notify_active()
        self.show_on_statusbar("Connected to Broker({})".format(str(rc)))
        
    def on_mqtt_disconnect(self, mqttc, userdata, rc):
        self.show_on_statusbar("Disconnected to Broker({})".format(str(rc)))
        
    def on_mqtt_message(self, mqttc, userdata, msg):
        mapi = str(msg.topic)
        
        try:
            if mapi in self.message_api.keys():
                payload = json.loads(msg.payload)
                if "app" not in payload:
                    print("message payload does not contain the app")
                    return
                
                if payload["app"] != APP_NAME:
                    self.message_api[mapi](payload)
            else:
                print("Unknown MAPI was called :", mapi)

        except json.JSONDecodeError as e:
            print("MAPI Message payload cannot be converted")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AVSimManager()
    window.show()
    sys.exit(app.exec())
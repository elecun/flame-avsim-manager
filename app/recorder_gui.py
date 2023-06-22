

import pathlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pygubu
from neon import eyetracker
from uvc_camera import camera
import json

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "flame-ui.ui"

class app_avsim_manager:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_path(PROJECT_PATH)
        self.master = master

        #devices
        self.camera0 = None
        self.camera1 = None
        self.camera2 = None
        self.camera3 = None
        self.camera4 = None
        self.camera5 = None
        self.eyetracker = eyetracker("192.168.0.7")

        self.builder.add_from_file(PROJECT_UI)
        self.mainwindow = self.builder.get_object('flame_ui_root', master)
        self.camera0_monitor = self.builder.get_object('camera1_canvas', master)
        self.builder.connect_callbacks(self)

    def __del__(self):
        print("close all devices")
        if self.camera0 != None:
            self.camera0.close()
        
        if self.eyetracker != None:
            self.eyetracker.close()

        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()

    # gui button event callback functions
    def camera1_connect(self):
        if self.camera0 == None:
            btn_camera_connect_label = self.builder.get_object('btn_camera1_connect', self.master)
            print("camera 1 opening..")
            self.camera0 = camera(0, tk_canvas=self.camera0_monitor)

    def camera2_connect(self):
        print("camera 2 connect ")
    def camera3_connect(self):
        print("camera 3 connect ")
    def camera4_connect(self):
        print("camera 4 connect ")
    def camera5_connect(self):
        print("camera 5 connect ")
    def camera6_connect(self):
        print("camera 6 connect ")

    # get eye tracker device info
    def eyetracker_discover(self):
        device_info = self.eyetracker.discover()
        info = json.loads(device_info)
        if info:
            label_eyetracker_ip = self.builder.get_object('label_eyetracker_ip', self.master)
            label_eyetracker_name = self.builder.get_object('label_eyetracker_name', self.master)
            label_eyetracker_battery = self.builder.get_object('label_eyetracker_battery', self.master)
            label_eyetracker_storage = self.builder.get_object('label_eyetracker_storage', self.master)
            label_eyetracker_ip.config(text=info["ip"])
            label_eyetracker_name.config(text=info["name"])
            label_eyetracker_battery.config(text="{}%".format(info["battery_level"]))
            label_eyetracker_storage.config(text=info["free_storage"])
            tk.messagebox.showinfo("Discover", "Found the NEON Eyetracker device")
        else:
            tk.messagebox.showerror("No Device Found", "NEON Eyetracker cannot be found. Please check the device network state.")

    def scenario_file_open(self):
        print("scenario file open")
    def eyetracker_record_start(self):
        if self.eyetracker:
            self.eyetracker.start_record()

    def eyetracker_record_stop(self):
        if self.eyetracker:
            if self.eyetracker.stop_record():
                tk.messagebox.showinfo("Eye Tracker", "Stopped Recording")
            else:
                tk.messagebox.showerror("Eye Tracker", "Error is occured to stop recording..")

    def scenario_run(self):
        print("scenario run")
    def scenario_step(self):
        print("scenarop step forward")
    def scenario_stop(self):
        print("scenario stop")


if __name__ == '__main__':
    app = app_avsim_manager()
    app.run()
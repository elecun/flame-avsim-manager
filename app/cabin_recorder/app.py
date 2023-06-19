

'''
Data Recorder
'''

import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.ttk import Label
from tkinter import PhotoImage
from tkinter import Button
import cv2
import datetime
import PIL.Image, PIL.ImageTk
import threading
import sys, os
from pathlib import Path
from uvc_camera import camera
from neon import eyetracker
import threading

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class neon_eyetracker:
    def __init__(self):
        pass

    def __del__(self):
        pass

class app_avsim_manager:
    def __init__(self, window, window_title) -> None:
        self.app_width = 2160
        self.app_height = 1020
        self.cameraview_width = 480
        self.cameraview_height = 270
        self.eyetrackerview_width = 585
        self.eyetrackerview_height = 500
        self.camera_0 = None
        self.camera_1 = None
        self.camera_2 = None
        self.camera_3 = None
        self.camera_4 = None
        self.camera_5 = None
        self.eyetracker = None
        
        self.camera_threads = []

        self.window = window
        self.window.title(window_title)
        self.window.geometry('{}x{}'.format(self.app_width, self.app_height))
        self.window.resizable(False, False)
        self.window.configure(bg = "#FFFFFF")

        self.main_canvas = tk.Canvas(self.window, bg = "#FFFFFF", height=self.app_height, width=self.app_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera0_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera1_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.eyetracker_canvas = tk.Canvas(self.window, bg = "#eeeeee", height=self.eyetrackerview_height, width=self.eyetrackerview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.main_canvas.place(x=0, y=0)
        self.camera0_canvas.place(x=38, y=52)
        self.camera1_canvas.place(x=518, y=52)
        self.eyetracker_canvas.place(x=1007, y=52)

        # button : record stop
        btn_record_stop_image = PhotoImage(file=relative_to_assets("record_stop.png"))
        btn_record_stop = Button(image=btn_record_stop_image,  borderwidth=1,  highlightthickness=2,  command=lambda: print("Data Record Stop"),  relief="flat")
        btn_record_stop.place(x=2005.0, y=964.0, width=114.0, height=35.0)

        # button : record start
        btn_record_start_image = PhotoImage(file=relative_to_assets("record_start.png"))
        btn_record_start = Button(image=btn_record_start_image,  borderwidth=1,  highlightthickness=2,  command=lambda: print("Data Record Start"),  relief="flat")
        btn_record_start.place(x=1875.0, y=964.0, width=114.0, height=35.0)

        # button : discover eyetracker
        btn_neon_discover_image = PhotoImage(file=relative_to_assets("neon_discover.png"))
        btn_neon_discover = Button(image=btn_neon_discover_image,  borderwidth=1,  highlightthickness=2,  command=lambda: print("Eyetracker Device discover"),  relief="flat")
        btn_neon_discover.place(x=1477.0, y=610.0, width=114.0, height=35.0)

        
        # Label
        Label(self.window,text = "In-Cabin Camera Monitoring", font=("Arial 9"), background="#9ce0f7").place(x=38, y=18)

        # Label for eyetracker
        Label(self.window,text = "Eye Tracker Monitoring", font=("Arial 9"), background="#9ce0f7").place(x=1005, y=18)
        Label(self.window,text = "Device IP Address : ", font=("Arial 9"), background="#f0f0f0").place(x=1010, y=58)
        self.neon_label_ip = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_ip.place(x=1220, y=58)

        Label(self.window,text = "Device Name : ", font=("Arial 9"), background="#f0f0f0").place(x=1010, y=83)
        self.neon_label_name = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_name.place(x=1220, y=83)

        Label(self.window,text = "Device SOC : ", font=("Arial 9"), background="#f0f0f0").place(x=1010, y=108)
        self.neon_label_soc = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_soc.place(x=1220, y=108)

        Label(self.window,text = "Device Free Storage : ", font=("Arial 9"), background="#f0f0f0").place(x=1010, y=133)
        self.neon_label_storage = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_storage.place(x=1220, y=133)

        Label(self.window,text = "Device Serial # : ", font=("Arial 9"), background="#f0f0f0").place(x=1010, y=158)
        self.neon_label_serial = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_serial.place(x=1220, y=158)


        # apply device
        # self.camera_0 = camera(0)
        # self.camera_1 = camera(2)
        # self.eyetracker = eyetracker()
        # self.eyetracker.discover()

        self.update()
        self.window.mainloop()

    def record(self):
        pass

    # image capture & grab
    def update(self):

        # camera 0 update
        if self.camera_0!=None:
            cam0_ret, cam0_raw = self.camera_0.grab(self.cameraview_width, self.cameraview_height)
            if cam0_ret:
                self.camera0_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam0_raw))
                self.camera0_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera0_image)

        # camera 1 updated
        if self.camera_1!=None:
            cam1_ret, cam1_raw = self.camera_1.grab(self.cameraview_width, self.cameraview_height)
            if cam1_ret:
                self.camera1_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam1_raw))
                self.camera1_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera1_image)

        self.window.after(30, self.update)

    def close(self):
        if self.camera_0!=None:
            self.camera_0.close()
        if self.camera_1!=None:
            self.camera_1.close()
        if self.eyetracker!=None:
            self.eyetracker.close()
        print("close all devices")


    def __del__(self):
        self.close()


if __name__=="__main__":
    app_avsim_manager(tk.Tk(), "AV Simulator Data Recorder")


'''
Data Recorder
'''

import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.ttk import Label
from tkinter import PhotoImage
from tkinter import Button
from tkinter import messagebox
import cv2
import datetime
import PIL.Image, PIL.ImageTk
import threading
import sys, os
from pathlib import Path
from uvc_camera import camera
from neon import eyetracker
import threading
import json

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

        self.app_width = 1940 # gui window size
        self.app_height = 1020 # gui window size
        self.cameraview_width = 480 # camera canvas size
        self.cameraview_height = 270 # camera canvas size
        self.eyetrackerview_width = 585 # eyetracker canvas size
        self.eyetrackerview_height = 500 # eyetracker canvas size
        self.camera0 = None
        self.camera1 = None
        self.camera2 = None
        self.camera3 = None
        self.camera4 = None
        self.camera5 = None
        self.eyetracker = eyetracker() # eyetracker device class instance

        self.window = window
        self.window.title(window_title)
        self.window.geometry('{}x{}'.format(self.app_width, self.app_height))
        self.window.resizable(False, False)
        self.window.configure(bg = "#FFFFFF")

        self.main_canvas = tk.Canvas(self.window, bg = "#FFFFFF", height=self.app_height, width=self.app_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.main_canvas.place(x=0, y=0)

        # draw boundary box
        self.main_canvas.create_rectangle(6, 5, 987+6, 992+5, fill='white', outline='black', width=1) # camera monitoring
        self.main_canvas.create_rectangle(1000, 5, 463+1000, 992+5, fill='white', outline='black', width=1) # eyetracker monitoring
        self.main_canvas.create_rectangle(1470, 5, 463+1470, 992+5, fill='white', outline='black', width=1) # scenario handling

        # Labels
        Label(self.window,text = "In-Cabin Camera", font=("Arial 9"), background="#ffffff").place(x=17, y=15)
        Label(self.window,text = "Eye Tracker", font=("Arial 9"), background="#ffffff").place(x=1005, y=18)

        # draw camera area
        self.camera0_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera1_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera2_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera3_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera4_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera5_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera0_canvas.place(x=17, y=52)
        self.camera1_canvas.place(x=504, y=52)
        self.camera2_canvas.place(x=17, y=368)
        self.camera3_canvas.place(x=504, y=368)
        self.camera4_canvas.place(x=17, y=684)
        self.camera5_canvas.place(x=504, y=684)

        # camera connector buttons
        self.btn_camera0_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda:self.camera_connect(0), repeatdelay=1000, repeatinterval=100)
        self.btn_camera0_connect.place(x=387, y=330)
        self.btn_camera1_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda: self.camera_connect(2), repeatdelay=1000, repeatinterval=100)
        self.btn_camera1_connect.place(x=874, y=330)
        self.btn_camera2_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda: print("connect"), repeatdelay=1000, repeatinterval=100)
        self.btn_camera2_connect.place(x=387, y=646)
        self.btn_camera3_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda: print("connect"), repeatdelay=1000, repeatinterval=100)
        self.btn_camera3_connect.place(x=874, y=646)
        self.btn_camera4_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda: print("connect"), repeatdelay=1000, repeatinterval=100)
        self.btn_camera4_connect.place(x=387, y=962)
        self.btn_camera5_connect = tk.Button(self.window, text="connect", borderwidth=1,  highlightthickness=1, overrelief="solid", width=10, command=lambda: print("connect"), repeatdelay=1000, repeatinterval=100)
        self.btn_camera5_connect.place(x=874, y=962)

        # eyetracker info labels
        Label(self.window,text = "Device IP : ", font=("Arial 9"), background="#ffffff").place(x=1010, y=58)
        Label(self.window,text = "Device Name : ", font=("Arial 9"), background="#ffffff").place(x=1010, y=83)
        Label(self.window,text = "Device SOC : ", font=("Arial 9"), background="#ffffff").place(x=1010, y=108)
        Label(self.window,text = "Device Free Storage(GBytes) : ", font=("Arial 9"), background="#ffffff").place(x=1010, y=133)

        self.neon_label_ip = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_ip.place(x=1150, y=58)
        self.neon_label_name = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_name.place(x=1170, y=83)
        self.neon_label_soc = tk.Label(self.window,text = "Not discovered", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_soc.place(x=1160, y=108)
        self.neon_label_storage = tk.Label(self.window,text = "-", font=("Arial 9"), background="#f0f0f0")
        self.neon_label_storage.place(x=1350, y=133)

        # eyetracker control buttons
        btn_neon_discover = Button(self.window, text="discover", borderwidth=1,  highlightthickness=1,  overrelief="solid", width=10, command=self.eyetracker_connect, repeatdelay=1000, repeatinterval=100)
        btn_neon_discover.place(x=1350.0, y=180)


        self.update()
        self.window.mainloop()

    def camera_connect(self, vid):
        if vid ==0:
            self.camera0 = camera(vid)
        elif vid==2:
            self.camera1 = camera(vid)

    # discover the eyetracker device
    def eyetracker_connect(self):
        eyetracker_info = self.eyetracker.discover()
        info = json.loads(eyetracker_info)
        if info:
            self.neon_label_ip.config(text=info["ip"])
            self.neon_label_name.config(text=info["name"])
            self.neon_label_soc.config(text="{}%".format(info["soc"]))
            self.neon_label_storage.config(text=info["free"])
        else:
            tk.messagebox.showerror("No Device Found", "NEON Eyetracker cannot be found. Please check the device network state.")
        

    def record(self):
        pass

    # image capture & grab
    def update(self):

        # camera 0 update
        if self.camera0!=None:
            cam0_ret, cam0_raw = self.camera0.grab(self.cameraview_width, self.cameraview_height)
            if cam0_ret:
                self.camera0_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam0_raw))
                self.camera0_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera0_image)

        # camera 1 updated
        if self.camera1!=None:
            cam1_ret, cam1_raw = self.camera1.grab(self.cameraview_width, self.cameraview_height)
            if cam1_ret:
                self.camera1_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam1_raw))
                self.camera1_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera1_image)

        self.window.after(30, self.update)

    def close(self):
        if self.camera0!=None:
            self.camera0.close()
        if self.camera1!=None:
            self.camera1.close()
        if self.eyetracker!=None:
            self.eyetracker.close()
        print("close all devices")

        self.window.quit()


    def __del__(self):
        self.close()


if __name__=="__main__":
    app_avsim_manager(tk.Tk(), "AV Simulator Data Recorder")
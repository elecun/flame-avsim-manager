

'''
Data Recorder
'''

import tkinter as tk
from tkinter import font
from tkinter import ttk
from tkinter.ttk import Label
import cv2
import datetime
import PIL.Image, PIL.ImageTk
import threading
import sys, os
from pathlib import Path
from uvc_camera import camera
import webview

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


class app_avsim_manager:
    def __init__(self, window, window_title) -> None:
        self.app_width = 2160
        self.app_height = 1020
        self.cameraview_width = 480
        self.cameraview_height = 270
        self.eyetrackerview_width = 585
        self.eyetrackerview_height = 600
        self.window = window
        self.window.title(window_title)
        self.window.geometry('{}x{}'.format(self.app_width, self.app_height))
        self.window.resizable(False, False)
        self.window.configure(bg = "#FFFFFF")

        self.main_canvas = tk.Canvas(self.window, bg = "#FFFFFF", height=self.app_height, width=self.app_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera0_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.camera1_canvas = tk.Canvas(self.window, bg = "#000000", height=self.cameraview_height, width=self.cameraview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.eyetracker_canvas = tk.Canvas(self.window, bg = "#000000", height=self.eyetrackerview_height, width=self.eyetrackerview_width, bd = 0, highlightthickness = 0, relief = "ridge")
        self.main_canvas.place(x=0, y=0)
        self.camera0_canvas.place(x=38, y=52)
        self.camera1_canvas.place(x=518, y=52)
        self.eyetracker_canvas.place(x=1007, y=52)
        
        self.main_canvas.create_text(38.0, 18.0, anchor="nw", text="In-Cabin Camera Monitoring", fill="#000000", font=("Inter", 15 * -1))
        self.main_canvas.create_text(1007.0, 18.0, anchor="nw", text="Eye Tracker Monitoring", fill="#000000", font=("Inter", 15 * -1))

        self.camera_0 = camera(0)
        self.camera_1 = camera(2)
        
        # self.eyetracker_canvas.create_window("test", 'https://www.naver.com')
        t = webview.create_window('test', 'https://www.naver.com')
        webview.start()

        self.update()
        self.window.mainloop()

    def record(self):
        pass

    # image capture & grab
    def update(self):
        cam0_ret, cam0_raw = self.camera_0.grab(self.cameraview_width, self.cameraview_height)
        cam1_ret, cam1_raw = self.camera_1.grab(self.cameraview_width, self.cameraview_height)
        if cam0_ret:
            self.camera0_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam0_raw))
            self.camera0_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera0_image)

        if cam1_ret:
            self.camera1_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cam1_raw))
            self.camera1_canvas.create_image(self.cameraview_width/2, self.cameraview_height/2, image = self.camera1_image)
        
        self.window.after(30, self.update)

    def close(self):
        self.camera_0.close()
        self.camera_1.close()


    def __del__(self):
        self.camera_0.close()
        self.camera_1.close()
        

# class uvc_camera:
#     def __init__(self, vid=0):
#         self.vid = vid
#         try:
#             self.camera = cv2.VideoCapture(vid)
#             if not self.camera.isOpened():
#                 raise ValueError("Unable to open camera device vid=",vid)
#         except ValueError as e:
#             return None
        
#         self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
#         self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
#         print("Camera device open id={} ({}x{})".format(vid, self.width, self.height))

#     def save(self, fps):
#         filename = str(datetime.datetime.now()) + ".mp4"
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         self.video = cv2.VideoWriter(filename, fourcc, fps/3.0, (self.width, self.height))

#     def grab(self, view_width, view_height):
#         if self.camera.isOpened():
#             ret, raw = self.camera.read()
#             if ret:
#                 resized = cv2.resize(raw, dsize=(view_width, view_height), interpolation=cv2.INTER_AREA)
#                 resized = cv2.putText(resized, "Camera {}".format(self.vid), (380,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
#                 return (ret, resized)
#             else:
#                 return (ret, None)
#         else:
#             return (False, None)
        
#     def close(self):
#         if self.camera.isOpened():
#             self.camera.release()
        
        
#     def __del__(self):
#         if self.camera.isOpened():
#             self.camera.release()


if __name__=="__main__":
    app_avsim_manager(tk.Tk(), "AV Simulator Data Recorder")
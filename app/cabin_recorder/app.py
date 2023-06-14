

'''
Data Recorder
'''

from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.ttk import Label
import cv2
import datetime
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self, window, window_title) -> None:
        self.window = window
        self.window.title(window_title)
        self.window.geometry('640x480+100+100')
        self.window.resizable(True, True)

        self.vid_0 = CabinCam_Capture(0)
        self.canvas = Canvas(self.window, width=self.vid_0.width, height=self.vid_0.height)
        self.canvas.pack()

        window_font=font.Font(family="Arial", size=20)

        # label_projectname = ttk.Label(app_window, text="Record project name : ", font=window_font)
        # editbox_projectname = Entry(app_window,width=30, font=window_font)
        # btn_record_start = Button(app_window, text="Record Start", fg="red")
        # btn_record_stop = Button(app_window, text="Record Stop", fg="red")
        # label_projectname.grid(column=0, row=0)
        # editbox_projectname.grid(column=1, row=0)
        # btn_record_start.grid(column=2, row=0)
        # btn_record_stop.grid(column=3, row=0)

        # self.fps = self.vid_0.get(cv2.CAP_PROP_FPS)
        # self.delay = round(1000.0/self.fps)
        self.update()

        self.window.mainloop()

    def record(self):
        pass

    def update(self):
        ret, raw = self.vid_0.grab()
        if ret:
            self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(raw))
            self.canvas.create_image(0, 0, image = self.image)
        self.window.after(1, self.update)

    def __del__(self):
        self.vid_0.camera.release()
        


class CabinCam_Capture:
    def __init__(self, vid=0):
        self.camera = cv2.VideoCapture(vid)
        if not self.camera.isOpened():
            raise ValueError("Unable to open camera vid=",vid)
        
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        #device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
        #device.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        #device.set(cv2.CAP_PROP_AUTO_WB, 0)

    def save(self, fps):
        filename = str(datetime.datetime.now()) + ".mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(filename, fourcc, fps/3.0, (self.width, self.height))

    def grab(self):
        if self.camera.isOpened():
            ret, raw = self.camera.read()
            if ret:
                return (ret, raw)
            else:
                return (ret, None)
        else:
            return (False, None)
        
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()


if __name__=="__main__":

    App(Tk(), "AV Simulator Data Recorder")

    # app_window.geometry('640x480+100+100')
    # app_window.resizable(True, True)

    # app = App(app_window)
    # app_window.mainloop()
    
    # # Menu Definition
    # app_menu = Menu(app_window)
    # menu_file_new = Menu(app_menu)
    # menu_file_new.add_command(label='New')
    # app_menu.add_cascade(label='File', menu=menu_file_new)

    # menu_window_show_camview = Menu(app_menu)
    # menu_window_show_camview.add_command(label='Show Camera View')
    # app_menu.add_cascade(label='Window', menu=menu_window_show_camview)

    # app_window.config(menu=app_menu)

    # app_window.mainloop()
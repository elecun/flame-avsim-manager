'''
UVC Camera Device Class with OpenCV
'''
import cv2
import datetime
import threading

class camera(threading.Thread):
    def __init__(self, vid=0, view_h=270, view_w=480):
        threading.Thread.__init__(self)
        self.vid = vid
        self.view_h = view_h
        self.view_w = view_w
        try:
            self.camera = cv2.VideoCapture(vid)
            if not self.camera.isOpened():
                raise ValueError("Unable to open camera device vid=",vid)
        except ValueError as e:
            return None
        
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Camera device open id={} ({}x{})".format(vid, self.width, self.height))
        self._thread_running = True
        
    def run(self):
        while self._thread_running:
            ret, raw = self.camera.read()
            if ret:
                resized = cv2.resize(raw, dsize=(self.view_w, self.view_h), interpolation=cv2.INTER_AREA)

    def stop(self):
        self._thread_running = False
        self.camera.release()            
        
    def save(self, fps):
        filename = str(datetime.datetime.now()) + ".mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(filename, fourcc, fps/3.0, (self.width, self.height))

    def grab(self, view_width, view_height):
        if self.camera.isOpened():
            ret, raw = self.camera.read()
            if ret:
                resized = cv2.resize(raw, dsize=(view_width, view_height), interpolation=cv2.INTER_AREA)
                resized = cv2.putText(resized, "Camera {}".format(self.vid), (380,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                return (ret, resized)
            else:
                return (ret, None)
        else:
            return (False, None)
        
    def close(self):
        if self.camera.isOpened():
            self.camera.release()
        
        
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()
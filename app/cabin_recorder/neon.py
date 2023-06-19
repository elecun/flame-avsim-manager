'''
Pupil Lab. NEON device class
'''
from pupil_labs.realtime_api.simple import discover_one_device
import nest_asyncio
nest_asyncio.apply()
import json
import time

class eyetracker:
    def __init__(self):
        self.device_info = {}
        self.device = None
        pass

    def discover(self) -> json:
        self.device = discover_one_device(max_search_duration_seconds=5)
        if self.device !=None:
            self.device_info["ip"] = self.device.phone_ip
            self.device_info["name"] = self.device.phone_name
            self.device_info["id"] = self.device.phone_id
            self.device_info["soc"] = str(self.device.battery_level_percent)
            self.device_info["free"] = str(int(self.device.memory_num_free_bytes/1024**3))
        return json.dumps(self.device_info)
    
    def start_record(self):
        if self.device:
            self.recording_id = self.device.recording_start()
            print(f"Started recording with id {self.recording_id}")
        else:
            print("cannot be started recording..")

    
    def close(self):
        if self.device != None:
            self.device.close()
            print("Close eyetracker device")
    
    def __del__(self):
        if self.device != None:
            self.device.close()

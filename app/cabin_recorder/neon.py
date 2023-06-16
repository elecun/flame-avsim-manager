'''
Pupil Lab. NEON device class
'''
from pupil_labs.realtime_api.simple import discover_one_device
import nest_asyncio
nest_asyncio.apply()

class eyetracker:
    def __init__(self):        
        pass

    def discover(self) -> bool:
        self.device = discover_one_device()
        if self.device !=None:
            print(f"Phone IP address: {self.device.phone_ip}")
            print(f"Phone name: {self.device.phone_name}")
            print(f"Battery level: {self.device.battery_level_percent}%")
            print(f"Free storage: {self.device.memory_num_free_bytes / 1024**3:.1f} GB")
            print(f"Serial number of connected glasses: {self.device.module_serial}")
            return True
        print("Eyetracker device is not discovered")
        return False
    
    def close(self):
        if self.device != None:
            self.device.close()
            print("Close eyetracker device")
    
    def __del__(self):
        if self.device != None:
            self.device.close()

'''
Pupil Lab. NEON device class
'''
import asyncio
from pupil_labs.realtime_api.simple import discover_one_device
from pupil_labs.realtime_api import Device, Network, StatusUpdateNotifier
import json
import time

class eyetracker:
    def __init__(self):
        self.device_info = {}
        self.device = None
        self.is_recording = False
        asyncio.run(self.update_status())

    def print_component(self, component):
        print(component)

    # device status update
    async def update_status(self):
        async with Network() as network:
            dev_info = await network.wait_for_new_device(timeout_seconds=5)
        if dev_info is None:
            print("No device could not be found")
            return
        
        async with Device.from_discovered_device(dev_info) as device:
            duration = 00
            print("starting auto-update for 10 seconds")
            notifier = StatusUpdateNotifier(device, callback=[self.print_component])
            await notifier.receive_updates_start()
            await asyncio.sleep(duration)
            print("Stopping auto-update")
            await notifier.receive_updates_stop()

    def discover(self) -> json:
        self.device = discover_one_device(max_search_duration_seconds=5)
        if self.device !=None:
            self.device_info["ip"] = self.device.phone_ip
            self.device_info["name"] = self.device.phone_name
            self.device_info["id"] = self.device.phone_id
            self.device_info["battery_level"] = str(self.device.battery_level_percent)
            self.device_info["battery_state"] = str(self.device.battery_state)
            self.device_info["free_storage"] = "{}".format(int(self.device.memory_num_free_bytes/1024**3),"GB")
            self.device_info["storage_level"] = str(self.device.memory_state)
        return json.dumps(self.device_info)
    
    def start_record(self):
        if self.device:
            self.recording_id = self.device.recording_start()
            self.is_recording = True
            print(f"Started recording with id {self.recording_id}")
        else:
            print("cannot be started recording..")

    def stop_record(self) -> bool:
        if self.device and self.is_recording==True:
            self.device.recording_stop_and_save()
            return True
        return False

    
    def close(self):
        if self.device != None:
            self.device.close()
            print("Close eyetracker device")
    
    def __del__(self):
        if self.device != None:
            self.device.close()

'''
Time Scheduler Class for Operation Scenario Manager
'''

from abc import *


# Interface Class
class Ischeduler(ABCMeta):
    
    @abstractmethod
    def set_schedule(self):
        pass
    
    @abstractmethod
    def go_next(self):
        pass
    
    
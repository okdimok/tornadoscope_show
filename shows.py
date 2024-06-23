from threading import Event, Lock
from show_elements import *

import logging
logger = logging.getLogger(__name__)

class Show:
    _current_show_element: ShowElement = None
    _needs_stop: Event = Event()
    _is_not_running: Event = Event()

    def __init__(self, elements=[], name="") -> None:
        self.elements = list(elements)
        self._is_not_running.set()
        self.name = name

    def __repr__(self) -> str:
        s = ""
        s += self.__str__()
        s += f"\nTotal {len(self.elements)} effects for {self.get_duration()} s\n"
        s += ",\n".join(str(se) for se in self.elements)
        return s

    async def run_once(self):
        self._is_not_running.clear()
        logger.info(f"#"*6 + f" Running {self}.")
        for se in self.elements:
            if self._needs_stop.is_set():
                break
            logger.info(f"#"*3 + f" launching {se}")
            self._current_show_element = se
            await se.run()
        self._is_not_running.set()
        cancelled = self._needs_stop.is_set()
        reason = "Canceled" if cancelled else "Finished"
        logger.debug(f"#"*6 + f" {reason} {self}.")
        return cancelled # returns, whether it has been cancelled (error 1), or everything is fine (0)

    def stop(self):
        logger.debug(f"#"*6 + f" Stopping {self}.")
        self._needs_stop.set()
        if self._current_show_element is not None: self._current_show_element.stop()
        self._is_not_running.wait()
        self._needs_stop.clear()
        logger.debug(f"#"*6 + f" Stopped {self}.")
    
    def wait(self):
        logger.debug(f"#"*6 + f" {self.wait.__name__} Waiting: {self}.")
        self._is_not_running.wait()
        logger.debug(f"#"*6 + f" {self.wait.__name__} Completed: {self}.")

    def is_running(self) -> bool:
        return not self._is_not_running.is_set()
        
    async def run_infinetely(self):
        while True:
            await self.run_once()
            if self._needs_stop.is_set():
                break

    def get_duration(self):
        return sum(e.duration for e in self.elements)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.name}"
    
    def set_device(self, device):
        self.device = device
        for se in self.elements:
            se.set_device(device)
    
class CoolTornado(NamingEnum):
    default = Show([
        StartRed(5),
        StartGreen(5)
    ])
    

CoolTornado.__init_names__()
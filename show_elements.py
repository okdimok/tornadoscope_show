from __future__ import annotations
from threading import Event, Timer, Lock, Thread
import time
import logging
from utils import dotdict, NamingEnum
from math import floor
from gyverhub_device import GHDevice
from tornadoscope_state import TornadoscopeVariables as tv, TornadoscopeState


logger = logging.getLogger(__name__)

class ShowElement:
    _sleep_timer: Timer
    _is_activating_lock: Lock = Lock()

    def __init__(self, duration: float):
        self.device = None
        self.duration = duration

    def sleep(self):
        self._sleep_timer = Timer(self.duration, lambda: True) # No name for timers:(  name=f"{self.__class__.__name__}_sleep_timer")
        self._sleep_timer.start()
        self._sleep_timer.join()

    async def activate(self):
        logger.debug("activating {self}")

    def deactivate(self):
        pass

    async def run(self):
        with self._is_activating_lock:
            await self.activate()
        self.sleep()
        self.deactivate()

    def stop(self):
        with self._is_activating_lock:
            try:
                self._sleep_timer.cancel() # it is OK to cancel Timer twice
            except Exception as e:
                logger.exception(f"Was unable to stop {self}: {e}")


    def __str__(self) -> str:
        return f"{self.__class__.__name__} for {self.duration} s"
    
    def set_device(self, device: GHDevice):
        self.device = device
    
class IterativeShowElementExample(ShowElement):
    def __init__(self, device: GHDevice, duration: float):
        super().__init__(device, duration)

    async def activate(self):
        # set initial state
        pass       

    def step_progress(self):
        step_every = self.duration/self.n_leds/len(self.current_progress)
        need_steps = floor((time.time() - self.last_step)/step_every)
        for i in range(need_steps):
            # make one step
            pass
        return self.duration < time.time() - self.last_step

    def iterate(self):
        if not True:
            logger.warning(f"{self}: no matching wleds connected.")
            return
        self.last_step = time.time()
        stop = False
        while not stop:
            stop = self.step_progress()
            time.sleep(1/60)

    def sleep(self):
        self._sleep_timer = Thread(target=self.iterate, args=[]) # No name for timers:(  name=f"{self.__class__.__name__}_sleep_timer")
        self._sleep_timer.start()
        self._sleep_timer.join()

    def deactivate(self):
        logging.debug("Deactivating sACN senders.")
        

class SetTornadoscopeState(ShowElement):
    def __init__(self, duration: float, tornadoscope_state: TornadoscopeState):
        super().__init__(duration)
        self.tornadoscope_state = tornadoscope_state

    async def activate(self):
        prev_state = self.device.tornadoscope_state
        diff = prev_state.diff(self.tornadoscope_state)
        state_diff, phase_diff = diff
        for k, v in state_diff.items():
            await self.device.set(k, v)
        for i, p in enumerate(phase_diff):
            if p:
                await self.device.set(tv.phase, i)
                for k, v in p.items():
                    await self.device.set(k, v)
        self.device.state = self.tornadoscope_state


class StartRed(SetTornadoscopeState):
    def __init__(self, duration: float):
        tornadoscope_state = TornadoscopeState.from_overrides(
            {
                tv.freq: 20,
            },
            [{
                tv.phase_state: 1,
                tv.phase_hue_val: 0,
            }]
        )
        super().__init__(duration, tornadoscope_state)

class StartGreen(SetTornadoscopeState):
    def __init__(self, duration: float):
        tornadoscope_state = TornadoscopeState.from_overrides(
            {
                tv.freq: 20,
            },
            [{
                tv.phase_state: 1,
                tv.phase_hue_val: 255 // 3,
            }]
        )
        super().__init__(duration, tornadoscope_state)



        


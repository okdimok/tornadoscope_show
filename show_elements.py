from threading import Event, Timer, Lock, Thread
import time
import logging
from math import floor

logger = logging.getLogger(__name__)

class ShowElement:
    _sleep_timer: Timer
    _is_activating_lock: Lock = Lock()

    def __init__(self, duration):
        self.duration = duration

    def sleep(self):
        self._sleep_timer = Timer(self.duration, lambda: True) # No name for timers:(  name=f"{self.__class__.__name__}_sleep_timer")
        self._sleep_timer.start()
        self._sleep_timer.join()

    def activate(self):
        logger.debug("activating {self}")

    def deactivate(self):
        pass

    def run(self):
        with self._is_activating_lock:
            self.activate()
        self.sleep()
        self.deactivate()

    def stop(self):
        with self._is_activating_lock:
            try:
                self._sleep_timer.cancel() # it is OK to cancel Timer twice
            except Exception as e:
                logger.exception(f"Was unable to stop {self}: {e}")


    def __str__(self) -> str:
        return f"{self.__class__.__name__}(pow {self.eff_intensity}, spd {self.eff_speed}) for {self.duration} s"
    
class IterativeShowElementExample(ShowElement):
    def __init__(self, duration):
        super().__init__(duration)

    def activate(self):
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

"""Alarm and timer functionality"""
import threading
import time
import logging
from datetime import datetime, timedelta
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class AlarmTimer:
    def __init__(self):
        self.timers = []
        self.alarms = []

    def set_timer(self, seconds: int, message: str = "Timer done!", callback: Optional[Callable] = None) -> str:
        def ring():
            time.sleep(seconds)
            if callback:
                callback(message)
            else:
                logger.info(message)
        t = threading.Thread(target=ring, daemon=True)
        t.start()
        self.timers.append(t)
        return f"Timer set for {seconds} seconds"

    def set_alarm(self, hour: int, minute: int, message: str = "Alarm!", callback: Optional[Callable] = None) -> str:
        def wait():
            while True:
                now = datetime.now()
                if now.hour == hour and now.minute == minute:
                    if callback:
                        callback(message)
                    else:
                        logger.info(message)
                    break
                time.sleep(30)
        t = threading.Thread(target=wait, daemon=True)
        t.start()
        self.alarms.append(t)
        return f"Alarm set for {hour:02d}:{minute:02d}"

    def stopwatch_start(self) -> str:
        self._stopwatch_start = time.time()
        return "Stopwatch started"

    def stopwatch_stop(self) -> str:
        elapsed = time.time() - getattr(self, '_stopwatch_start', time.time())
        return f"Elapsed: {int(elapsed)} seconds"

alarm_timer = AlarmTimer()

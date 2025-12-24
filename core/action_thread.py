from PyQt6.QtCore import QThread
import time

from services.action_mapper import ACTION_MAP


class ActionThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = True

        self.current_gesture = "NONE"
        self.last_executed_gesture = None
        self.last_action_time = 0

        # Cooldown between same actions (seconds)
        self.COOLDOWN = 1.5

    def set_gesture(self, gesture):
        self.current_gesture = gesture

    def run(self):
        while self.running:
            now = time.time()

            # Ignore invalid gestures
            if self.current_gesture == "NONE":
                self.last_executed_gesture = None
                time.sleep(0.01)
                continue

            # Fire only on NEW gesture OR after cooldown
            if (
                self.current_gesture in ACTION_MAP
                and (
                    self.current_gesture != self.last_executed_gesture
                    or now - self.last_action_time >= self.COOLDOWN
                )
            ):
                ACTION_MAP[self.current_gesture]()
                self.last_executed_gesture = self.current_gesture
                self.last_action_time = now

            time.sleep(0.01)

    def stop(self):
        self.running = False

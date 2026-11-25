import threading
import tkinter as tk
from queue import Empty, SimpleQueue

import RPi.GPIO as GPIO

STEP_PINS = (12, 16, 20, 21)
SEQUENCE = (
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 1, 0, 0),
    (1, 0, 0, 0),
)


class StepperApp:
    def __init__(self, root):
        self.root = root
        self.direction = 1
        self.delay = 0.0051
        self.step = 0
        self.stop_event = threading.Event()
        self.errors = SimpleQueue()
        self.worker = None

        root.title("스텝 모터 제어")
        directions = tk.Frame(root)
        directions.pack(padx=10, pady=10)
        self.clockwise = tk.Button(
            directions, text="시계 방향", command=lambda: self.set_direction(1)
        )
        self.clockwise.pack(side=tk.LEFT, padx=5)
        self.counterclockwise = tk.Button(
            directions, text="반시계 방향", command=lambda: self.set_direction(-1)
        )
        self.counterclockwise.pack(side=tk.LEFT, padx=5)
        self.set_direction(1)

        self.button = tk.Button(root, text="시작", width=12, command=self.toggle)
        self.button.pack(pady=5)
        speed = tk.Scale(
            root, from_=1, to=100, orient=tk.HORIZONTAL, label="속도", command=self.set_speed
        )
        speed.set(50)
        speed.pack(pady=5)
        self.status = tk.Label(root, text="정지")
        self.status.pack(pady=10)
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(50, self.check_worker)

    def set_direction(self, direction):
        self.direction = direction
        self.clockwise.config(relief=tk.SUNKEN if direction == 1 else tk.RAISED)
        self.counterclockwise.config(relief=tk.SUNKEN if direction == -1 else tk.RAISED)

    def set_speed(self, value):
        self.delay = (101 - int(value)) / 10000

    def toggle(self):
        if self.worker is not None:
            self.stop_event.set()
            self.button.config(text="정지 중", state=tk.DISABLED)
            return
        self.stop_event.clear()
        self.button.config(text="정지")
        self.status.config(text="작동 중")
        self.worker = threading.Thread(target=self.run_motor)
        self.worker.start()

    def run_motor(self):
        try:
            while not self.stop_event.is_set():
                GPIO.output(STEP_PINS, SEQUENCE[self.step])
                self.step = (self.step + self.direction) % len(SEQUENCE)
                self.stop_event.wait(self.delay)
        except (OSError, RuntimeError) as error:
            self.errors.put(str(error))
        finally:
            GPIO.output(STEP_PINS, GPIO.LOW)

    def check_worker(self):
        if self.worker is not None and not self.worker.is_alive():
            self.worker = None
            self.button.config(text="시작", state=tk.NORMAL)
            try:
                self.status.config(text=f"GPIO 오류: {self.errors.get_nowait()}")
            except Empty:
                self.status.config(text="정지")
        self.root.after(50, self.check_worker)

    def close(self):
        self.root.destroy()


def main():
    root = tk.Tk()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STEP_PINS, GPIO.OUT, initial=GPIO.LOW)
    try:
        app = StepperApp(root)
        try:
            root.mainloop()
        finally:
            app.stop_event.set()
            if app.worker is not None:
                app.worker.join()
    finally:
        GPIO.cleanup(STEP_PINS)


if __name__ == "__main__":
    main()

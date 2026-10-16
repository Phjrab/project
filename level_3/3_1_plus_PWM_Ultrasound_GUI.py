import RPi.GPIO as GPIO
import time
import tkinter as tk
import threading
from queue import Queue, Empty

TRIG = 23
ECHO = 24
ECHO_TIMEOUT = 0.05


class DistanceMeasurementApp:
    def __init__(self, master):
        self.master = master
        master.title("초음파 거리 측정")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ECHO, GPIO.IN)
        self.distance_label = tk.Label(master, text="거리: - cm", font=("Helvetica", 24))
        self.distance_label.pack(pady=20)
        self.toggle_button = tk.Button(master, text="측정 시작", command=self.toggle_measurement)
        self.toggle_button.pack(pady=10)
        self.is_measuring = False
        self.is_closing = False
        self.measurement_thread = None
        self.stop_event = threading.Event()
        self.results = Queue()
        self.master.after(30, self.process_results)

    def toggle_measurement(self):
        if self.is_measuring:
            self.stop_measurement()
        else:
            self.start_measurement()

    def start_measurement(self):
        if self.is_closing or (self.measurement_thread and self.measurement_thread.is_alive()):
            return
        self.stop_event.clear()
        self.is_measuring = True
        self.toggle_button.config(text="측정 중지")
        self.measurement_thread = threading.Thread(target=self.measure_distance, daemon=True)
        self.measurement_thread.start()

    def stop_measurement(self):
        self.is_measuring = False
        self.stop_event.set()
        self.toggle_button.config(text="측정 시작", state=tk.DISABLED)
        self.wait_for_worker()

    def wait_for_worker(self):
        if self.measurement_thread and self.measurement_thread.is_alive():
            self.master.after(20, self.wait_for_worker)
            return
        if self.is_closing:
            GPIO.cleanup((TRIG, ECHO))
            self.master.destroy()
        else:
            self.toggle_button.config(state=tk.NORMAL)

    def wait_for_echo(self, level):
        deadline = time.monotonic() + ECHO_TIMEOUT
        while GPIO.input(ECHO) != level:
            if self.stop_event.is_set() or time.monotonic() >= deadline:
                return None
            if self.stop_event.wait(0.00001):
                return None
        if self.stop_event.is_set():
            return None
        return time.monotonic()

    def measure_distance(self):
        try:
            while not self.stop_event.is_set():
                GPIO.output(TRIG, False)
                if self.stop_event.wait(0.1):
                    break
                GPIO.output(TRIG, True)
                time.sleep(0.00001)
                GPIO.output(TRIG, False)
                pulse_start = self.wait_for_echo(1)
                pulse_end = self.wait_for_echo(0) if pulse_start is not None else None
                if self.stop_event.is_set():
                    break
                if pulse_start is None or pulse_end is None:
                    self.results.put("거리: 신호 없음")
                else:
                    distance = (pulse_end - pulse_start) * 34300 / 2
                    self.results.put(f"거리: {distance:.1f} cm")
                if self.stop_event.wait(0.1):
                    break
        except Exception as error:
            self.results.put(f"오류: {error}")
        finally:
            GPIO.output(TRIG, False)

    def process_results(self):
        latest = None
        try:
            while True:
                latest = self.results.get_nowait()
        except Empty:
            pass
        if latest is not None and self.is_measuring and not self.is_closing:
            self.distance_label.config(text=latest)
        if self.is_measuring and self.measurement_thread and not self.measurement_thread.is_alive():
            self.is_measuring = False
            self.toggle_button.config(text="측정 시작", state=tk.NORMAL)
        if not self.is_closing:
            self.master.after(30, self.process_results)

    def quit(self):
        if self.is_closing:
            return
        self.is_closing = True
        self.stop_measurement()


def main():
    root = tk.Tk()
    app = DistanceMeasurementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()


if __name__ == "__main__":
    main()

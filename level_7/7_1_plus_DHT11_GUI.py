import threading
import tkinter as tk
from queue import Empty, SimpleQueue

import adafruit_dht
import board


class DHT11App:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        self.results = SimpleQueue()
        self.worker = None
        self.closing = False

        root.title("DHT11 센서 모니터링")
        self.temperature = tk.Label(root, text="온도: - °C", font=("Helvetica", 16))
        self.temperature.pack(padx=20, pady=(12, 5))
        self.humidity = tk.Label(root, text="습도: - %", font=("Helvetica", 16))
        self.humidity.pack(pady=5)
        self.status = tk.Label(root, text="대기 중", wraplength=230)
        self.status.pack(padx=10, pady=5)
        self.button = tk.Button(root, text="시작", width=12, command=self.toggle)
        self.button.pack(pady=(0, 12))
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(50, self.update_display)

    def toggle(self):
        if self.worker is not None:
            self.stop_event.set()
            self.button.config(text="정지 중", state=tk.DISABLED)
            return
        self.stop_event.clear()
        self.status.config(text="측정 중")
        self.button.config(text="정지")
        self.worker = threading.Thread(target=self.read_sensor)
        self.worker.start()

    def read_sensor(self):
        try:
            sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)
            try:
                while not self.stop_event.is_set():
                    try:
                        self.results.put((sensor.temperature, sensor.humidity))
                    except RuntimeError as error:
                        self.results.put(f"센서 읽기 오류: {error}")
                        self.stop_event.wait(2)
                    else:
                        self.stop_event.wait(3)
            finally:
                sensor.exit()
        except (OSError, RuntimeError, ValueError) as error:
            self.results.put(f"DHT11 오류: {error}")

    def update_display(self):
        if self.closing:
            return
        latest = None
        try:
            while True:
                latest = self.results.get_nowait()
        except Empty:
            pass

        if isinstance(latest, str) and not self.stop_event.is_set():
            self.status.config(text=latest)
        elif isinstance(latest, tuple) and not self.stop_event.is_set():
            temperature, humidity = latest
            self.temperature.config(text=f"온도: {temperature:.1f} °C")
            self.humidity.config(text=f"습도: {humidity:.1f} %")
            self.status.config(text="측정 중")

        if self.worker is not None and not self.worker.is_alive():
            self.worker = None
            self.button.config(text="시작", state=tk.NORMAL)
            if self.stop_event.is_set():
                self.status.config(text="측정 중지")
        self.root.after(50, self.update_display)

    def close(self):
        if self.closing:
            return
        self.closing = True
        self.stop_event.set()
        self.button.config(state=tk.DISABLED)
        self.finish_close()

    def finish_close(self):
        if self.worker is not None and self.worker.is_alive():
            self.root.after(20, self.finish_close)
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DHT11App(root)
    try:
        root.mainloop()
    finally:
        app.stop_event.set()
        if app.worker is not None:
            app.worker.join()

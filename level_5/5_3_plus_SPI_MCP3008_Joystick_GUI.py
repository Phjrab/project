import threading
import tkinter as tk
from queue import Empty, SimpleQueue

import spidev

X_CHANNEL = 1
Y_CHANNEL = 2
SW_CHANNEL = 0
CANVAS_SIZE = 200
DOT_RADIUS = 10


def read_adc(spi, channel):
    response = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((response[1] & 3) << 8) | response[2]


class JoystickApp:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        self.results = SimpleQueue()
        self.worker = None
        self.closing = False

        root.title("조이스틱 모니터")
        self.values = tk.Label(root, text="X: 0\nY: 0\nSW: 0")
        self.values.pack(pady=5)
        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
        self.canvas.pack(padx=10, pady=5)
        self.dot = self.canvas.create_oval(90, 90, 110, 110, fill="red", outline="")
        self.status = tk.Label(root, text="")
        self.status.pack()
        self.button = tk.Button(root, text="시작", width=12, command=self.toggle)
        self.button.pack(pady=10)
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(50, self.update_display)

    def toggle(self):
        if self.worker is not None:
            self.stop_event.set()
            self.button.config(text="정지 중", state=tk.DISABLED)
            return
        self.stop_event.clear()
        self.status.config(text="")
        self.button.config(text="정지")
        self.worker = threading.Thread(target=self.read_joystick)
        self.worker.start()

    def read_joystick(self):
        spi = spidev.SpiDev()
        try:
            spi.open(0, 0)
            spi.max_speed_hz = 100_000
            while not self.stop_event.is_set():
                x = read_adc(spi, X_CHANNEL)
                y = read_adc(spi, Y_CHANNEL)
                switch = read_adc(spi, SW_CHANNEL)
                self.results.put((x, y, switch))
                self.stop_event.wait(0.1)
        except OSError as error:
            self.results.put(f"SPI 오류: {error}")
        finally:
            spi.close()

    def update_display(self):
        if self.closing:
            return
        latest = None
        try:
            while True:
                latest = self.results.get_nowait()
        except Empty:
            pass

        if isinstance(latest, str):
            self.status.config(text=latest)
        elif latest is not None and not self.stop_event.is_set():
            x, y, switch = latest
            self.values.config(text=f"X: {x}\nY: {y}\nSW: {switch}")
            width = CANVAS_SIZE - 2 * DOT_RADIUS
            px = x / 1023 * width
            py = (1023 - y) / 1023 * width
            self.canvas.coords(self.dot, px, py, px + 2 * DOT_RADIUS, py + 2 * DOT_RADIUS)

        if self.worker is not None and not self.worker.is_alive():
            self.worker = None
            self.button.config(text="시작", state=tk.NORMAL)
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
    app = JoystickApp(root)
    try:
        root.mainloop()
    finally:
        app.stop_event.set()
        if app.worker is not None:
            app.worker.join()

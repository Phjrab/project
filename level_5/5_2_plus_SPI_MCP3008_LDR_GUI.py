import tkinter as tk
from collections import deque
from queue import Empty, Queue
from threading import Event, Thread

import spidev

LDR_CHANNEL = 0
WIDTH = 400
HEIGHT = 200


class LDRApp:
    def __init__(self, root, spi):
        self.root = root
        self.spi = spi
        self.samples = deque(maxlen=50)
        self.results = Queue()
        self.stop_event = Event()
        self.worker = None
        self.closing = False

        root.title("LDR 센서 모니터")
        self.label = tk.Label(root, text="LDR 값: -", font=("Helvetica", 16))
        self.label.pack(pady=10)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.button = tk.Button(root, text="시작", width=10, command=self.toggle)
        self.button.pack(pady=10)

        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(50, self.process_results)

    def toggle(self):
        if self.worker is not None:
            self.stop_event.set()
            self.button.config(text="정지 중", state=tk.DISABLED)
            return

        self.stop_event.clear()
        self.worker = Thread(target=self.read_ldr, daemon=True)
        self.button.config(text="정지")
        self.worker.start()

    def read_ldr(self):
        try:
            while not self.stop_event.is_set():
                response = self.spi.xfer2([1, (8 + LDR_CHANNEL) << 4, 0])
                value = ((response[1] & 3) << 8) | response[2]
                self.results.put(value)
                self.stop_event.wait(0.5)
        except OSError as error:
            self.results.put(f"SPI 오류: {error}")

    def process_results(self):
        worker_done = self.worker is not None and not self.worker.is_alive()
        try:
            while True:
                result = self.results.get_nowait()
                if not self.closing:
                    if isinstance(result, int):
                        self.label.config(text=f"LDR 값: {result}")
                        self.update_graph(result)
                    else:
                        self.label.config(text=result)
        except Empty:
            pass

        if worker_done:
            self.worker = None
            self.button.config(text="시작", state=tk.NORMAL)

        if self.closing and self.worker is None:
            self.root.destroy()
            return

        self.root.after(50, self.process_results)

    def update_graph(self, value):
        self.samples.append(value)
        self.canvas.delete("all")
        if len(self.samples) == 1:
            x = WIDTH / 2
            y = HEIGHT - 3 - value * (HEIGHT - 6) / 1023
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="blue")
            return

        x_step = (WIDTH - 6) / (len(self.samples) - 1)
        points = []
        for index, sample in enumerate(self.samples):
            x = 3 + index * x_step
            y = HEIGHT - 3 - sample * (HEIGHT - 6) / 1023
            points.extend((x, y))
        self.canvas.create_line(*points, fill="blue")

    def close(self):
        self.closing = True
        self.stop_event.set()
        self.button.config(state=tk.DISABLED)


def main():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    try:
        spi.max_speed_hz = 100_000
        root = tk.Tk()
        LDRApp(root, spi)
        root.mainloop()
    finally:
        spi.close()


if __name__ == "__main__":
    main()

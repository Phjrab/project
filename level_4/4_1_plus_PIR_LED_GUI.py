"""PIR motion monitor: GPIO4 input, GPIO20 red, GPIO21 yellow."""

import time
import tkinter as tk

import RPi.GPIO as GPIO

RED_PIN = 20
YELLOW_PIN = 21
PIR_PIN = 4
POLL_MS = 100
WARMUP_SECONDS = 5


class PIRMonitorApp:
    def __init__(self, master):
        self.master = master
        self.running = False
        self.closing = False
        self.after_id = None
        master.title("PIR 움직임 감지")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIR_PIN, GPIO.IN)
        self.ready_at = time.monotonic() + WARMUP_SECONDS

        self.status_label = tk.Label(master, text="감지 중지", font=("Helvetica", 22))
        self.status_label.pack(padx=30, pady=(20, 10))
        self.value_label = tk.Label(master, text="PIR 값: -", font=("Helvetica", 14))
        self.value_label.pack()

        self.canvas = tk.Canvas(master, width=300, height=110, highlightthickness=0)
        self.canvas.pack(pady=10)
        self.red_light = self.canvas.create_oval(45, 5, 105, 65, fill="gray")
        self.yellow_light = self.canvas.create_oval(195, 5, 255, 65, fill="gray")
        self.canvas.create_text(75, 90, text="빨강 · 움직임 없음")
        self.canvas.create_text(225, 90, text="노랑 · 움직임 감지")

        self.toggle_button = tk.Button(master, text="감지 시작", width=16, command=self.toggle)
        self.toggle_button.pack(pady=5)
        tk.Button(master, text="종료", width=16, command=self.quit).pack(pady=(5, 20))
        master.protocol("WM_DELETE_WINDOW", self.quit)

    def set_leds(self, red, yellow):
        GPIO.output(RED_PIN, red)
        GPIO.output(YELLOW_PIN, yellow)
        self.canvas.itemconfig(self.red_light, fill="red" if red else "gray")
        self.canvas.itemconfig(self.yellow_light, fill="yellow" if yellow else "gray")

    def toggle(self):
        if self.closing:
            return
        if self.running:
            self.stop()
        else:
            self.running = True
            self.toggle_button.config(text="감지 중지")
            self.poll()

    def poll(self):
        self.after_id = None
        if not self.running or self.closing:
            return
        remaining = self.ready_at - time.monotonic()
        if remaining > 0:
            self.status_label.config(text=f"센서 준비 중 ({int(remaining) + 1}초)")
        else:
            try:
                detected = bool(GPIO.input(PIR_PIN))
                self.set_leds(not detected, detected)
            except Exception as error:
                self.stop()
                self.status_label.config(text=f"센서 오류: {error}")
                return
            self.value_label.config(text=f"PIR 값: {int(detected)}")
            self.status_label.config(text="움직임 감지!" if detected else "움직임 없음")
        self.after_id = self.master.after(POLL_MS, self.poll)

    def stop(self):
        self.running = False
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None
        self.set_leds(False, False)
        self.status_label.config(text="감지 중지")
        self.value_label.config(text="PIR 값: -")
        self.toggle_button.config(text="감지 시작")

    def quit(self):
        if self.closing:
            return
        self.closing = True
        try:
            self.stop()
        finally:
            try:
                GPIO.cleanup((RED_PIN, YELLOW_PIN, PIR_PIN))
            finally:
                self.master.destroy()


def main():
    root = tk.Tk()
    app = PIRMonitorApp(root)
    try:
        root.mainloop()
    finally:
        app.quit()


if __name__ == "__main__":
    main()

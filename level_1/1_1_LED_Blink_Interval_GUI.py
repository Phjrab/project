import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import messagebox


class LEDControlApp:
    def __init__(self, master):
        self.master = master
        master.title("LED Control 1.1")

        self.led_pin = 4
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

        tk.Label(master, text="LED 깜빡임 횟수:").pack()
        self.count_entry = tk.Entry(master)
        self.count_entry.pack()

        tk.Label(master, text="깜빡임 간격 (초):").pack()
        self.interval_entry = tk.Entry(master)
        self.interval_entry.pack()

        tk.Button(master, text="시작", command=self.start_blinking).pack()
        tk.Button(master, text="종료", command=self.quit).pack()

    def start_blinking(self):
        try:
            blink_count = int(self.count_entry.get())
            interval = float(self.interval_entry.get())

            if blink_count <= 0 or interval <= 0:
                raise ValueError

            for _ in range(blink_count):
                GPIO.output(self.led_pin, GPIO.HIGH)
                self.master.update()
                time.sleep(interval)

                GPIO.output(self.led_pin, GPIO.LOW)
                self.master.update()
                time.sleep(interval)

            messagebox.showinfo(
                "완료",
                f"LED가 {blink_count}번 깜빡였습니다. (간격: {interval}초)",
            )
        except ValueError:
            messagebox.showerror(
                "오류",
                "횟수는 1 이상의 정수, 간격은 0보다 큰 숫자로 입력해 주세요.",
            )

    def quit(self):
        GPIO.cleanup()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LEDControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()

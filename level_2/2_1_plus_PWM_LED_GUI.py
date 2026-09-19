import RPi.GPIO as GPIO
import tkinter as tk
import threading
import time

LED_PIN = 18
PWM_FREQUENCY = 50


class PWMLEDApp:
    def __init__(self, master):
        self.master = master
        self.master.title("자동 PWM 제어")

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
        self.pwm.start(0)

        self.running_event = threading.Event()
        self.stop_event = threading.Event()
        self.worker = None

        self.duty_label = tk.Label(master, text="Duty cycle: 0%", font=("Helvetica", 14))
        self.duty_label.pack(pady=(20, 10))

        self.period_label = tk.Label(master, text="PWM 주기: 20ms (50Hz)")
        self.period_label.pack(pady=10)

        self.control_button = tk.Button(master, text="시작", width=14, command=self.toggle_running)
        self.control_button.pack(pady=15)

        self.quit_button = tk.Button(master, text="종료", width=14, command=self.quit)
        self.quit_button.pack(pady=(0, 20))

        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    def toggle_running(self):
        if self.running_event.is_set():
            self.running_event.clear()
            self.control_button.config(text="시작")
        else:
            self.running_event.set()
            self.control_button.config(text="정지")

            if self.worker is None or not self.worker.is_alive():
                self.worker = threading.Thread(target=self.change_brightness, daemon=True)
                self.worker.start()

    def change_brightness(self):
        while not self.stop_event.is_set():
            if not self.running_event.wait(timeout=0.1):
                continue

            for duty_cycle in list(range(0, 101, 5)) + list(range(100, -1, -5)):
                if self.stop_event.is_set():
                    return

                while not self.running_event.is_set():
                    if self.stop_event.wait(0.05):
                        return

                self.pwm.ChangeDutyCycle(duty_cycle)
                self.master.after(0, self.update_duty_label, duty_cycle)

                if self.stop_event.wait(0.1):
                    return

    def update_duty_label(self, duty_cycle):
        self.duty_label.config(text=f"Duty cycle: {duty_cycle}%")

    def quit(self):
        self.stop_event.set()
        self.running_event.set()

        if self.worker is not None and self.worker.is_alive():
            self.worker.join(timeout=1)

        self.pwm.stop()
        del self.pwm
        GPIO.cleanup()
        self.master.destroy()


def main():
    root = tk.Tk()
    PWMLEDApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

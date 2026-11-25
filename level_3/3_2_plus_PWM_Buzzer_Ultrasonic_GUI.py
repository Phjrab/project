import RPi.GPIO as GPIO
import time
import tkinter as tk
import threading
from queue import Queue, Empty

TRIG = 23
ECHO = 24
BUZZER = 18
ALARM_DISTANCE = 50
SCALE = [262, 294, 330, 349, 392, 440, 493, 523]
ECHO_TIMEOUT = 0.05


class UltrasonicAlarmApp:
    def __init__(self, master):
        self.master = master
        master.title("초음파 거리 측정 · 부저 경보")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)
        self.pwm = GPIO.PWM(BUZZER, 100)
        self.pwm.start(0)
        self.distance_label = tk.Label(master, text="거리: - cm", font=("Helvetica", 24))
        self.distance_label.pack(pady=20)
        self.status_label = tk.Label(master, text="대기 중 · 경보 기준 50cm 이하", font=("Helvetica", 14))
        self.status_label.pack(pady=10)
        self.toggle_button = tk.Button(master, text="측정 시작", command=self.toggle_measurement)
        self.toggle_button.pack(pady=10)
        self.quit_button = tk.Button(master, text="종료", command=self.quit)
        self.quit_button.pack(pady=10)
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
        while not self.results.empty():
            self.results.get_nowait()
        self.stop_event.clear()
        self.status_label.config(text="측정 중", fg="black")
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
            self.pwm.stop()
            GPIO.cleanup((TRIG, ECHO, BUZZER))
            self.master.destroy()
        else:
            self.toggle_button.config(state=tk.NORMAL)
            self.status_label.config(text="측정 중지 · 부저 꺼짐", fg="black")

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
                    self.pwm.ChangeDutyCycle(0)
                    self.results.put(("거리: 신호 없음", "센서 신호 확인", "gray"))
                else:
                    distance = (pulse_end - pulse_start) * 34300 / 2
                    alarm = distance <= ALARM_DISTANCE
                    self.results.put((f"거리: {distance:.1f} cm", "물체 감지! 경보음 발생" if alarm else "안전 거리 · 부저 꺼짐", "red" if alarm else "green"))
                    if alarm:
                        self.play_alarm()
                    else:
                        self.pwm.ChangeDutyCycle(0)
                if self.stop_event.wait(0.1):
                    break
        except Exception as error:
            self.results.put(("거리: - cm", f"오류: {error}", "red"))
        finally:
            self.pwm.ChangeDutyCycle(0)
            GPIO.output(TRIG, False)

    def play_alarm(self):
        try:
            for frequency in SCALE:
                if self.stop_event.is_set():
                    break
                self.pwm.ChangeFrequency(frequency)
                self.pwm.ChangeDutyCycle(50)
                if self.stop_event.wait(0.1):
                    break
        finally:
            self.pwm.ChangeDutyCycle(0)

    def process_results(self):
        latest = None
        try:
            while True:
                latest = self.results.get_nowait()
        except Empty:
            pass
        if latest is not None and self.is_measuring and not self.is_closing:
            distance_text, status_text, color = latest
            self.distance_label.config(text=distance_text)
            self.status_label.config(text=status_text, fg=color)
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
    app = UltrasonicAlarmApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()


if __name__ == "__main__":
    main()

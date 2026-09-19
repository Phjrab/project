import RPi.GPIO as GPIO
import tkinter as tk
import threading
from queue import Queue, Empty

BUZZER_PIN = 12
SCALE = [262, 294, 330, 349, 392, 440, 494, 523]
NOTE_NAMES = ["도", "레", "미", "파", "솔", "라", "시", "도"]
NOTE_DURATION = 0.5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


class ScalePlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("음계 재생기")
        self.master.resizable(False, False)

        self.pwm = GPIO.PWM(BUZZER_PIN, 100)
        self.is_playing = False
        self.closing = False
        self.stop_event = threading.Event()
        self.worker = None
        self.events = Queue()
        self.note_buttons = []

        self.play_button = tk.Button(
            master, text="음계 재생", width=16, command=self.play_scale
        )
        self.play_button.pack(pady=(14, 10))

        note_frame = tk.Frame(master)
        note_frame.pack(padx=10)
        for index, note in enumerate(NOTE_NAMES):
            button = tk.Button(
                note_frame,
                text=note,
                width=5,
                command=lambda i=index: self.play_note(i),
            )
            button.pack(side=tk.LEFT, padx=2)
            self.note_buttons.append(button)

        self.status_label = tk.Label(master, text="대기 중", width=26)
        self.status_label.pack(pady=14)

        self.quit_button = tk.Button(master, text="종료", width=12, command=self.quit)
        self.quit_button.pack(pady=(0, 14))

        self.master.after(50, self.process_events)

    def set_buttons(self, state):
        self.play_button.config(state=state)
        for button in self.note_buttons:
            button.config(state=state)

    def start_playback(self, target, args=()):
        if self.is_playing or self.closing:
            return
        self.is_playing = True
        self.stop_event.clear()
        self.set_buttons(tk.DISABLED)
        self.worker = threading.Thread(target=target, args=args, daemon=True)
        self.worker.start()

    def play_scale(self):
        self.start_playback(self._play_scale_worker)

    def play_note(self, index):
        self.start_playback(self._play_note_worker, (index,))

    def _play_scale_worker(self):
        try:
            self.pwm.start(10)
            for note, frequency in zip(NOTE_NAMES, SCALE):
                if self.stop_event.is_set():
                    break
                self.pwm.ChangeFrequency(frequency)
                self.events.put(("status", f"{note} 재생 중"))
                if self.stop_event.wait(NOTE_DURATION):
                    break
        finally:
            self.pwm.ChangeDutyCycle(0)
            self.events.put(("finished", None))

    def _play_note_worker(self, index):
        try:
            self.pwm.start(10)
            self.pwm.ChangeFrequency(SCALE[index])
            self.events.put(("status", f"{NOTE_NAMES[index]} 재생 중"))
            self.stop_event.wait(NOTE_DURATION)
        finally:
            self.pwm.ChangeDutyCycle(0)
            self.events.put(("finished", None))

    def process_events(self):
        try:
            while True:
                event, value = self.events.get_nowait()
                if event == "status" and not self.closing:
                    self.status_label.config(text=value)
                elif event == "finished":
                    self.finish_playback()
        except Empty:
            pass

        if not self.closing:
            self.master.after(50, self.process_events)

    def finish_playback(self):
        self.is_playing = False
        if not self.closing:
            self.status_label.config(text="대기 중")
            self.set_buttons(tk.NORMAL)

    def quit(self):
        if self.closing:
            return
        self.closing = True
        self.stop_event.set()
        if self.worker and self.worker.is_alive():
            self.worker.join(timeout=1)
        self.pwm.stop()
        del self.pwm
        GPIO.cleanup()
        self.master.destroy()


def main():
    root = tk.Tk()
    app = ScalePlayerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()


if __name__ == "__main__":
    main()

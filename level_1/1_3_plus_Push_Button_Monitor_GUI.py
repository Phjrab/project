import RPi.GPIO as GPIO
import tkinter as tk

BUTTON_PIN = 15  # BCM GPIO15, physical pin 10


class PushButtonApp:
    def __init__(self, master):
        self.master = master
        master.title("PUSH 버튼 모니터")

        self.label = tk.Label(master, text="버튼 상태: 대기 중")
        self.label.pack(pady=20)

        self.button_count = 0
        self.count_label = tk.Label(master, text="버튼 누른 횟수: 0")
        self.count_label.pack(pady=10)

        self.quit_button = tk.Button(master, text="종료", command=self.quit)
        self.quit_button.pack(pady=10)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.last_state = GPIO.input(BUTTON_PIN)
        self.is_running = True
        self.monitor_button()

    def monitor_button(self):
        current_state = GPIO.input(BUTTON_PIN)

        # LOW → HIGH가 되는 버튼 누름 순간만 한 번 카운트한다.
        if current_state == GPIO.HIGH and self.last_state == GPIO.LOW:
            self.button_count += 1
            self.label.config(text="버튼 상태: 눌림")
            self.count_label.config(text=f"버튼 누른 횟수: {self.button_count}")

        if current_state == GPIO.LOW and self.last_state == GPIO.HIGH:
            self.label.config(text="버튼 상태: 대기 중")

        self.last_state = current_state
        if self.is_running:
            self.master.after(30, self.monitor_button)

    def quit(self):
        self.is_running = False
        GPIO.cleanup()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PushButtonApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()

import RPi.GPIO as GPIO
import tkinter as tk

BUTTON_PIN = 15
LED_PIN = 4


class LEDControlApp:
    def __init__(self, master):
        self.master = master
        self.master.title("LED 제어")
        self.light_on = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.LOW)

        self.label = tk.Label(master, text="LED 상태: 꺼짐", font=("Helvetica", 16))
        self.label.pack(pady=15)

        self.led_image = tk.Canvas(master, width=100, height=100, highlightthickness=0)
        self.led_image.pack(pady=10)
        self.update_led_image()

        self.toggle_button = tk.Button(
            master,
            text="LED 상태 변경",
            command=self.toggle_led,
        )
        self.toggle_button.pack(pady=10)

        self.quit_button = tk.Button(master, text="종료", command=self.quit)
        self.quit_button.pack(pady=(0, 15))

        GPIO.add_event_detect(
            BUTTON_PIN,
            GPIO.RISING,
            callback=self.button_callback,
            bouncetime=300,
        )

    def button_callback(self, channel):
        self.master.after(0, self.toggle_led)

    def toggle_led(self):
        self.light_on = not self.light_on
        GPIO.output(LED_PIN, GPIO.HIGH if self.light_on else GPIO.LOW)
        self.update_led_status()

    def update_led_status(self):
        status = "켜짐" if self.light_on else "꺼짐"
        self.label.config(text=f"LED 상태: {status}")
        self.update_led_image()

    def update_led_image(self):
        self.led_image.delete("all")
        color = "yellow" if self.light_on else "gray"
        self.led_image.create_oval(10, 10, 90, 90, fill=color, outline="")

    def quit(self):
        GPIO.cleanup()
        self.master.destroy()


def main():
    root = tk.Tk()
    LEDControlApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

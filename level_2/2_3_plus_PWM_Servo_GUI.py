import RPi.GPIO as GPIO
import tkinter as tk
import threading

SERVO_PIN = 14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

class ServoControlApp:
    def __init__(self, master):
        self.master = master
        master.title("서보모터 제어")


        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.btn_0 = tk.Button(self.button_frame, text="0도", command=lambda: self.move_servo(2.5))
        self.btn_0.pack(side=tk.LEFT, padx=5)

        self.btn_90 = tk.Button(self.button_frame, text="90도", command=lambda: self.move_servo(7.5))
        self.btn_90.pack(side=tk.LEFT, padx=5)

        self.btn_180 = tk.Button(self.button_frame, text="180도", command=lambda: self.move_servo(12.5))
        self.btn_180.pack(side=tk.LEFT, padx=5)

        self.angle_slider = tk.Scale(master, from_=0, to=180, orient=tk.HORIZONTAL, command=self.slider_changed, length=300)
        self.angle_slider.pack(pady=10)


        self.status_label = tk.Label(master, text="대기 중")
        self.status_label.pack(pady=10)

    def move_servo(self, duty_cycle):
        def _move():
            servo.ChangeDutyCycle(duty_cycle)
            self.status_label.config(text=f"서보모터 각도: {self.duty_to_angle(duty_cycle)}도")

        threading.Thread(target=_move).start()

    def slider_changed(self, angle):
        duty = self.angle_to_duty(float(angle))
        self.move_servo(duty)

    def angle_to_duty(self, angle):
        return (angle / 18) + 2.5

    def duty_to_angle(self, duty):
        return (duty - 2.5) * 18

    def quit(self):
        servo.stop()
        GPIO.cleanup()
        self.master.quit()

def main():
    root = tk.Tk()
    app = ServoControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.quit)
    root.mainloop()

if __name__ == "__main__":
    main()

import RPi.GPIO as GPIO
import time

BUTTON_PIN = 15  # BCM GPIO15, physical pin 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("버튼을 누르면 'Button pushed!'가 출력됩니다. 종료: Ctrl+C")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            print("Button pushed!")
            time.sleep(0.1)  # polling delay and simple debounce
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

import RPi.GPIO as GPIO
import time

button_pin = 15
led_pin = 4
light_on = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

last_button_state = GPIO.input(button_pin)

print("버튼을 누를 때마다 LED가 켜지고 꺼집니다. 종료: Ctrl+C")

try:
    while True:
        current_button_state = GPIO.input(button_pin)

        if current_button_state == GPIO.HIGH and last_button_state == GPIO.LOW:
            light_on = not light_on
            GPIO.output(led_pin, GPIO.HIGH if light_on else GPIO.LOW)
            print("LED ON!" if light_on else "LED OFF!")
            time.sleep(0.3)

        last_button_state = current_button_state
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")

finally:
    GPIO.cleanup()

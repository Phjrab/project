import RPi.GPIO as GPIO
import time

LED_PIN = 18
PWM_FREQUENCY = 50

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
pwm.start(0)

print("PWM LED 밝기 변화가 시작됩니다. 종료: Ctrl+C")

try:
    while True:
        for duty_cycle in range(0, 101, 5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)

        for duty_cycle in range(100, -1, -5):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")

finally:
    pwm.stop()
    del pwm
    GPIO.cleanup()

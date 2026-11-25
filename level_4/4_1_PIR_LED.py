import RPi.GPIO as GPIO
import time

led_R = 20
led_Y = 21
sensor = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)

print("PIR Ready . . . . ")
time.sleep(5)

try:
    while True:
        print("PIR Sensor value : ", GPIO.input(sensor))
        if GPIO.input(sensor) == 1:
            GPIO.output(led_Y, 1)
            GPIO.output(led_R, 0)
            print("Motion Detected !")
            time.sleep(0.2)

        if GPIO.input(sensor) == 0:
            GPIO.output(led_R, 1)
            GPIO.output(led_Y, 0)
            print("Motion ended !")
            time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

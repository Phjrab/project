#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time

SERVO_PIN = 14 #서보모터 제어 핀 (물리 8번)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT) #출력설정

servo = GPIO.PWM(SERVO_PIN,50) # PWM 인스턴스 servo 생성, 주파수 50Hz
servo.start(0) # PWM 듀티비 0으로 시작

try:
    while True:
        # 듀티비를 변경하여 서보모터를 원하는 만큼 회전
        servo.ChangeDutyCycle(7.5)  # 90도
        time.sleep(1)
        servo.ChangeDutyCycle(12.5) # 180도
        time.sleep(1)
        servo.ChangeDutyCycle(2.5)  # 0도
        time.sleep(1)

except KeyboardInterrupt:
        servo.stop()
        GPIO.cleanup()

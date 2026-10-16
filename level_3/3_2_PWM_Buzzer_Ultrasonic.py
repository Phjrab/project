import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


TRIG = 23
ECHO = 24
BUZZER = 18


GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)


p = GPIO.PWM(BUZZER, 100)


Frq = [262, 294, 330, 349, 392, 440, 493, 523]
p.start(0)


def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2
    return distance


def play_alarm():
    for fr in Frq:
        p.ChangeFrequency(fr)
        p.ChangeDutyCycle(50)
        time.sleep(0.1)
    p.ChangeDutyCycle(0)


try:
    print("거리 측정 및 경보 시스템 시작")
    while True:
        dist = measure_distance()
        print(f"거리: {dist:.1f} cm")

        if dist <= 50:
            print("물체 감지! 경보음 발생")
            play_alarm()
        else:
            time.sleep(0.5)

except KeyboardInterrupt:
    print("사용자에 의해 프로그램 종료")
finally:
    p.stop()
    GPIO.cleanup()
    print("GPIO 리소스 정리 완료")

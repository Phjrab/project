import time

import RPi.GPIO as GPIO

STEP_PINS = (12, 16, 20, 21)
SEQUENCE = (
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 1, 0, 0),
    (1, 0, 0, 0),
)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(STEP_PINS, GPIO.OUT, initial=GPIO.LOW)
    step = 0
    try:
        print("스텝 모터 역방향 회전. 종료: Ctrl+C")
        while True:
            GPIO.output(STEP_PINS, SEQUENCE[step])
            step = (step - 1) % len(SEQUENCE)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nStopped by User")
    finally:
        GPIO.output(STEP_PINS, GPIO.LOW)
        GPIO.cleanup(STEP_PINS)


if __name__ == "__main__":
    main()

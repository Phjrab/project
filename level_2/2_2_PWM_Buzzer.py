import RPi.GPIO as GPIO
import time

BUZZER_PIN = 12
PWM_FREQUENCY = 100
SCALE = [262, 294, 330, 349, 392, 440, 494, 523]
NOTE_NAMES = ["도", "레", "미", "파", "솔", "라", "시", "도"]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = None

try:
    pwm = GPIO.PWM(BUZZER_PIN, PWM_FREQUENCY)
    pwm.start(10)

    print("도레미파솔라시도를 재생합니다. 종료: Ctrl+C")
    for note, frequency in zip(NOTE_NAMES, SCALE):
        print(f"{note}: {frequency}Hz")
        pwm.ChangeFrequency(frequency)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n사용자가 프로그램을 중단했습니다.")

except Exception as error:
    print(f"오류 발생: {error}")

finally:
    if pwm is not None:
        pwm.stop()
        del pwm
    GPIO.cleanup()
    print("GPIO가 정리되었습니다.")

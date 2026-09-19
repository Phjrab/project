import RPi.GPIO as GPIO
import time

BUTTON_PIN = 15  # BCM GPIO15, physical pin 10


def button_pressed_callback(channel):
    print("Button pushed!")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# LOW → HIGH로 바뀌는 순간에만 콜백 함수를 실행한다.
GPIO.add_event_detect(
    BUTTON_PIN,
    GPIO.RISING,
    callback=button_pressed_callback,
    bouncetime=200,
)

print("프로그램이 실행 중입니다. 버튼을 눌러보세요. 종료: Ctrl+C")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
finally:
    GPIO.cleanup()
    print("GPIO가 정리되었습니다.")

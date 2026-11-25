# Raspberry Pi GPIO Practice

## Level 1 — GPIO LED와 Push Button

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 1 | `1_LED_Blink_GUI.py` | 입력한 횟수만큼 LED 점멸 | [사진](level_1/images/1/) |
| 1-1 | `1_1_LED_Blink_Interval_GUI.py` | 점멸 횟수와 간격 입력 | [사진](level_1/images/1-1/) |
| 1-2 | `1_2_Button_Polling.py` | Polling 방식 버튼 감지 | [사진](level_1/images/1-2/) |
| 1-2+ | `1_2_plus_Button_Monitor_GUI.py` | 버튼 상태 GUI 표시 | [사진](level_1/images/1-2+/) |
| 1-3 | `1_3_Button_Event.py` | Rising event 방식 버튼 감지 | [사진](level_1/images/1-3/) |
| 1-3+ | `1_3_plus_Push_Button_Monitor_GUI.py` | 버튼 상태와 누른 횟수 GUI 표시 | [사진](level_1/images/1-3+/) |
| 1-4 | `1_4_Button_LED_Toggle.py` | 버튼 입력으로 LED ON/OFF 전환 | [사진](level_1/images/1-4/) |
| 1-4+ | `1_4_plus_Button_LED_GUI.py` | 버튼·GUI 버튼으로 LED 상태와 색상 표시 | [사진](level_1/images/1-4+/) |

실습 캡처 목록은 [level_1/images/README.md](level_1/images/README.md)에서 확인할 수 있다.

## 핀 연결

- LED: BCM GPIO4 (물리 7번) → 1 kΩ 저항 → LED 양극, LED 음극 → GND (물리 6번)
- Push button: 3.3V (물리 1번) ↔ 택트 스위치 ↔ BCM GPIO15 (물리 10번)

버튼은 브레드보드 중앙 홈을 가로질러 놓고, 3.3V와 GPIO15를 서로 다른 쪽의 대각선 핀에 연결한다.
## Level 2 — PWM 제어

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 2-1 | `2_1_PWM_LED.py` | PWM으로 LED 밝기 변화 | [사진·영상](level_2/images/2-1/) |
| 2-1+ | `2_1_plus_PWM_LED_GUI.py` | 시작·정지 GUI로 LED 밝기 변화 | [사진](level_2/images/2-1+/) |
| 2-2 | `2_2_PWM_Buzzer.py` | PWM 주파수로 무작위 음계 반복 재생 | [사진](level_2/images/2-2/) |
| 2-2+ | 2_2_plus_PWM_Buzzer_GUI.py | 음계·개별 음 재생 GUI | [사진](level_2/images/2-2+/) |
| 2-3 | [2_3_PWM_Servo.py](level_2/2_3_PWM_Servo.py) | 서보모터 90° → 180° → 0° 반복, 각 위치에서 1초 대기 | [배선 사진](level_2/images/2-3/) |
| 2-3+ | [2_3_plus_PWM_Servo_GUI.py](level_2/2_3_plus_PWM_Servo_GUI.py) | 0°·90°·180° 버튼과 각도 슬라이더 GUI | [GUI 사진](level_2/images/2-3+/) |
| 2-3+ ver2 | [2_3_plus_PWM_Servo_GUI_ver2.py](level_2/2_3_plus_PWM_Servo_GUI_ver2.py) | 시계·반시계 방향 버튼을 누르는 동안 5°씩 변경 | 실행 확인 전 |

2-3과 2-3+는 8주차 강의자료 코드를 바탕으로 신호 핀을 BCM GPIO14(물리 8번)로 변경했다. 서보모터 배선과 실행 방법은 [Level 2 README](level_2/README.md)에서 확인할 수 있다.

## Level 3 — 초음파 거리 측정

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 3.1 | [3_1_PWM_UltraSound.py](level_3/3_1_PWM_UltraSound.py) | 초음파 거리 측정 터미널 출력 | [사진](level_3/images/3-1/) |
| 3.1+ | [3_1_plus_PWM_Ultrasound_GUI.py](level_3/3_1_plus_PWM_Ultrasound_GUI.py) | 측정 시작·중지 GUI, ECHO 시간 제한과 중지 시 멈춤 수정 | [사진](level_3/images/3-1+/) |
| 3.2 | [3_2_PWM_Buzzer_Ultrasonic.py](level_3/3_2_PWM_Buzzer_Ultrasonic.py) | 50cm 이하에서 부저 음계 재생 | [사진](level_3/images/3-2/) |
| 3.2+ (3.9+ GUI) | [3_2_plus_PWM_Buzzer_Ultrasonic_GUI.py](level_3/3_2_plus_PWM_Buzzer_Ultrasonic_GUI.py) | 초음파 거리와 부저 경보 상태를 GUI에 표시 | |

배선과 실행 방법은 [Level 3 README](level_3/README.md)를 참고한다.

## Level 4 — PIR 인체 감지

| 실습 | 파일 | 내용 |
| --- | --- | --- |
| 4.1 | [4_1_PIR_LED.py](level_4/4_1_PIR_LED.py) | PIR 감지 상태로 LED 전환 |
| 4.1+ | [4_1_plus_PIR_LED_GUI.py](level_4/4_1_plus_PIR_LED_GUI.py) | PIR 감지 및 LED 상태를 GUI에 표시 |

## Level 5 — SPI 아날로그 입력

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 5.1 | [5_1_SPI_MCP3008.py](level_5/5_1_SPI_MCP3008.py) | 가변저항의 ADC 값과 전압 출력 | |
| 5.1+ | [5_1_plus_SPI_MCP3008_GUI.py](level_5/5_1_plus_SPI_MCP3008_GUI.py) | 가변저항 측정값을 GUI에 표시 | |
| 5.2 | [5_2_SPI_MCP3008_LDR.py](level_5/5_2_SPI_MCP3008_LDR.py) | 조도 센서의 ADC 값 출력 | |
| 5.2+ | [5_2_plus_SPI_MCP3008_LDR_GUI.py](level_5/5_2_plus_SPI_MCP3008_LDR_GUI.py) | 조도 센서 측정값을 그래프로 표시 | |
| 5.3 | [5_3_SPI_MCP3008_Joystick.py](level_5/5_3_SPI_MCP3008_Joystick.py) | MCP3008 CH1·CH2·CH0에서 조이스틱 X·Y·SW 읽기 | [실행 화면·배선·코드 캡처](level_5/images/5-3/) |
| 5.3+ | [5_3_plus_SPI_MCP3008_Joystick_GUI.py](level_5/5_3_plus_SPI_MCP3008_Joystick_GUI.py) | 조이스틱 위치와 버튼 상태를 GUI에 표시 | |

## Level 6 — 스텝 모터

| 실습 | 파일 | 내용 |
| --- | --- | --- |
| 6.1 | [6_1_Stepper_Forward.py](level_6/6_1_Stepper_Forward.py) | 정방향 회전 |
| 6.2 | [6_2_Stepper_Reverse.py](level_6/6_2_Stepper_Reverse.py) | 역방향 회전 |
| 6+ | [6_plus_Stepper_GUI.py](level_6/6_plus_Stepper_GUI.py) | GUI에서 회전 방향 및 정지 제어 |

## Level 7 — DHT11 온습도 센서

| 실습 | 파일 | 데이터 핀과 설정 |
| --- | --- | --- |
| 7.1 | [7_1_DHT11.py](level_7/7_1_DHT11.py) | GPIO17 (물리 11번), `use_pulseio=True` |
| 7.1+ | [7_1_plus_DHT11_GUI.py](level_7/7_1_plus_DHT11_GUI.py) | GPIO4 (물리 7번), `use_pulseio=False` |

## Level 8 — Flask 웹 서버

| 실습 | 파일 | 내용 |
| --- | --- | --- |
| 웹 서버 | [FASLK.PY](level_8/FASLK.PY) | 5000번 포트의 Hello, Flask! 화면 |
| 정적 라우팅 | [8_1_Flask_Routing.py](level_8/8_1_Flask_Routing.py) | `/`, `/name`, `/age`, `/job` 응답 |
| 주소로 LED 제어 | [flaskTest.py](level_8/flaskTest.py) | `/on`, `/off`, `/led/<state>` 경로로 제어 |
| 웹 버튼으로 LED 제어 | [8_1_flaskTest_web.py](level_8/8_1_flaskTest_web.py) | `/data`의 on, off, clean, Restart 버튼 |

## 카메라

### 사진 촬영

저장소 루트에서 실행하면 JPEG 파일이 `camera/photos/`에 저장된다.

```bash
mkdir -p camera/photos
for n in 1 2 3; do
    sudo rpicam-jpeg --nopreview --timeout 2000 \
        --output "camera/photos/photo_$(date +%Y%m%d_%H%M%S)_$n.jpg" || break
done
```

### 동영상 촬영

[picam.py](camera/picam.py)를 실행하고 파일 이름을 입력하면 H.264 영상이 `camera/videos/`에 저장된다.

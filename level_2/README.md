# Level 2 — PWM 제어

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 2-1 | `2_1_PWM_LED.py` | 50 Hz PWM으로 LED 밝기를 0%부터 100%까지 반복 변화 | [사진·영상](images/2-1/) |
| 2-1+ | `2_1_plus_PWM_LED_GUI.py` | 시작·정지·종료 GUI와 Duty cycle 표시 | [사진](images/2-1+/) |
| 2-2 | 2_2_PWM_Buzzer.py | PWM 주파수로 도레미파솔라시도 재생 | [사진](images/2-2/) |
| 2-3 | [2_3_PWM_Servo.py](2_3_PWM_Servo.py) | 서보모터 90° → 180° → 0° 반복, 각 위치에서 1초 대기 | 캡처 미등록 |
| 2-3+ | [2_3_plus_PWM_Servo_GUI.py](2_3_plus_PWM_Servo_GUI.py) | 0°·90°·180° 버튼과 각도 슬라이더 GUI | 캡처 미등록 |

## 핀 연결

- PWM 신호: BCM GPIO18 (물리 12번) → 1 kΩ 저항 → LED 양극
- GND: 물리 6번 → LED 음극
- 부저 모듈: VCC → 3.3V(물리 1번), I/O → BCM GPIO12(물리 32번), GND → 물리 34번
- 서보모터(2-3 / 2-3+): 빨강 VCC → 5V(물리 4번), 갈색/검정 GND → 물리 6번, 주황/노랑 신호 → BCM GPIO14(물리 8번)

## 서보모터 코드와 실행

8주차 강의자료의 2.3 및 2.3+ 코드를 옮기고, 사용자 배선에 맞춰 `SERVO_PIN`만 GPIO18에서 GPIO14로 변경했다. 시계·반시계 방향 버튼을 누르는 동안 이동하는 추가 과제는 포함하지 않는다.

2-3 기본 코드:

```bash
cd ~/embedded_project
sg dialout -c 'python3 level_2/2_3_PWM_Servo.py'
```

2-3+ GUI 코드:

```bash
cd ~/embedded_project
sg dialout -c 'python3 level_2/2_3_plus_PWM_Servo_GUI.py'
```

코드 문법 확인과 라파 파일 복사는 완료했다. 실제 모터 동작 및 GUI 실행 결과는 아직 확인하지 않았다.

## 실행 기록

- [터미널 실행 화면](images/2-1/01_terminal_execution.png)
- [PWM LED 밝기 변화 영상 (MP4)](images/2-1/02_pwm_led_brightness.mp4)
- [2-2 부저 음계 재생 터미널](images/2-2/01_terminal_execution.png)
- [2-2 부저 모듈 배선](images/2-2/02_buzzer_module_wiring.png)
- [2-2+ 음계 재생 GUI](images/2-2+/01_buzzer_gui.png)

실습 사진·영상 목록은 [level_2/images/README.md](images/README.md)에서 확인할 수 있다.


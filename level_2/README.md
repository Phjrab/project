# Level 2 — PWM 제어

| 실습 | 파일 | 내용 | 기록 |
| --- | --- | --- | --- |
| 2-1 | `2_1_PWM_LED.py` | 50 Hz PWM으로 LED 밝기를 0%부터 100%까지 반복 변화 | [사진·영상](images/2-1/) |
| 2-1+ | `2_1_plus_PWM_LED_GUI.py` | 시작·정지·종료 GUI와 Duty cycle 표시 | [사진](images/2-1+/) |
| 2-2 | 2_2_PWM_Buzzer.py | PWM 주파수로 도레미파솔라시도 재생 | [사진](images/2-2/) |

## 핀 연결

- PWM 신호: BCM GPIO18 (물리 12번) → 1 kΩ 저항 → LED 양극
- GND: 물리 6번 → LED 음극
- 부저 모듈: VCC → 3.3V(물리 1번), I/O → BCM GPIO12(물리 32번), GND → 물리 34번

## 실행 기록

- [터미널 실행 화면](images/2-1/01_terminal_execution.png)
- [PWM LED 밝기 변화 영상 (MP4)](images/2-1/02_pwm_led_brightness.mp4)
- [2-2 부저 음계 재생 터미널](images/2-2/01_terminal_execution.png)
- [2-2 부저 모듈 배선](images/2-2/02_buzzer_module_wiring.png)


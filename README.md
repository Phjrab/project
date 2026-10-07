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
| 2-2 | `2_2_PWM_Buzzer.py` | PWM 주파수로 도레미파솔라시도 재생 | [사진](level_2/images/2-2/) |
| 2-2+ | 2_2_plus_PWM_Buzzer_GUI.py | 음계·개별 음 재생 GUI | [사진](level_2/images/2-2+/) |
| 2-3 | [2_3_PWM_Servo.py](level_2/2_3_PWM_Servo.py) | 서보모터 90° → 180° → 0° 반복, 각 위치에서 1초 대기 | 캡처 미등록 |
| 2-3+ | [2_3_plus_PWM_Servo_GUI.py](level_2/2_3_plus_PWM_Servo_GUI.py) | 0°·90°·180° 버튼과 각도 슬라이더 GUI | 캡처 미등록 |

2-3과 2-3+는 8주차 강의자료 코드를 바탕으로 신호 핀을 BCM GPIO14(물리 8번)로 변경했다. 서보모터 배선과 실행 방법은 [Level 2 README](level_2/README.md)에서 확인할 수 있다.

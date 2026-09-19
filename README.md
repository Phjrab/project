# Raspberry Pi GPIO Practice

## Level 1 - GPIO LED와 Push Button

| 실습 | 파일 | 내용 |
| --- | --- | --- |
| 1 | `1_LED_Blink_GUI.py` | LED를 입력 횟수만큼 점멸 |
| 1-1 | `1_1_LED_Blink_Interval_GUI.py` | 점멸 횟수와 간격 입력 |
| 1-2 | `1_2_Button_Polling.py` | 버튼 입력을 Polling 방식으로 확인 |
| 1-2+ | `1_2_plus_Button_Monitor_GUI.py` | 버튼 상태 GUI 표시 |
| 1-3 | `1_3_Button_Event.py` | Rising event 방식 버튼 감지 |
| 1-3+ | `1_3_plus_Push_Button_Monitor_GUI.py` | 버튼 상태와 누른 횟수 GUI 표시 |

## 핀 연결

- LED: BCM GPIO4 (물리 7번) → 저항 → LED 양극, LED 음극 → GND (물리 6번)
- Push button: 3.3V (물리 1번) ↔ 택트 스위치 ↔ BCM GPIO15 (물리 10번)

버튼은 브레드보드 중앙 홈을 가로질러 놓고, 3.3V와 GPIO15를 서로 다른 쪽의 대각선 핀에 연결한다.


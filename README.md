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




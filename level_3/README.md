# Level 3 — 초음파 센서 HC-SR04

| 실습 | 파일 | 동작 |
| --- | --- | --- |
| 3.1 | `3_1_PWM_UltraSound.py` | 거리 측정값을 cm 단위로 출력 |
| 3.1+ | `3_1_plus_PWM_Ultrasound_GUI.py` | 시작·중지 GUI 및 신호 대기 시간 제한 |
| 3.2 | `3_2_PWM_Buzzer_Ultrasonic.py` | 50cm 이하 감지 시 부저 재생 |

## 배선

코드는 BCM 번호를 사용한다.

| 부품 | 신호 | 라파 연결 |
| --- | --- | --- |
| HC-SR04 | VCC | 5V, 물리 2번 |
| HC-SR04 | GND | GND, 물리 6번 |
| HC-SR04 | TRIG | GPIO23, 물리 16번 |
| HC-SR04 | ECHO | 저항 분압을 거쳐 GPIO24, 물리 18번 |
| 3핀 부저 | VCC | 3.3V, 물리 1번 |
| 3핀 부저 | GND | GND, 물리 14번 |
| 3핀 부저 | I/O | GPIO18, 물리 12번 |

ECHO는 5V 신호이므로 GPIO에 직접 연결하지 않는다. ECHO에서 1kΩ 저항을 거친 접점을 GPIO24에 연결하고, 접점에서 2kΩ 저항을 GND로 연결한다.

## 실행

라파 터미널에서 한 번에 하나씩 실행한다. GUI는 원격 데스크톱의 터미널에서 실행한다.

```bash
cd ~/embedded_project
sg dialout -c 'python3 level_3/3_1_PWM_UltraSound.py'
sg dialout -c 'python3 level_3/3_1_plus_PWM_Ultrasound_GUI.py'
sg dialout -c 'python3 level_3/3_2_PWM_Buzzer_Ultrasonic.py'
```

터미널 프로그램은 Ctrl+C로 종료한다.

## 기록

- [3.1 코드 캡처·거리 출력·연결 사진](images/3-1/)
- [3.1+ GUI 대기·측정 화면](images/3-1+/)
- [3.2 경보 출력·연결 사진](images/3-2/)

3.1+는 원본 강의 코드의 중지 시 멈춤을 수정했다. ECHO 대기에 0.05초 제한을 두고, 작업 스레드는 큐로 결과를 전달하며 GUI가 화면을 갱신한다.
실행 사진은 사용자가 제공한 기록이며, 거리 정확도나 경보음의 실제 음향 측정을 뜻하지 않는다.

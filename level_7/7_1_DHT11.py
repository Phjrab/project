import time

import adafruit_dht
import board

MAX_RETRIES = 5
RETRY_DELAY = 2
MEASUREMENT_INTERVAL = 3


def read_sensor(sensor):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return sensor.temperature, sensor.humidity
        except RuntimeError as error:
            print(f"센서 읽기 오류 ({attempt}/{MAX_RETRIES}): {error}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    return None


def main():
    sensor = adafruit_dht.DHT11(board.D17, use_pulseio=True)
    try:
        while True:
            reading = read_sensor(sensor)
            if reading is not None:
                temperature, humidity = reading
                print(f"온도: {temperature:.1f} °C | 습도: {humidity:.1f} %")
            time.sleep(MEASUREMENT_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped by User")
    finally:
        sensor.exit()


if __name__ == "__main__":
    main()

import time

import spidev

X_CHANNEL = 1
Y_CHANNEL = 2
SW_CHANNEL = 0


def read_adc(spi, channel):
    response = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((response[1] & 3) << 8) | response[2]


def main():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    try:
        spi.max_speed_hz = 100_000
        while True:
            x = read_adc(spi, X_CHANNEL)
            y = read_adc(spi, Y_CHANNEL)
            switch = read_adc(spi, SW_CHANNEL)
            print(f"X: {x}, Y: {y}, SW: {switch}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped by User")
    finally:
        spi.close()


if __name__ == "__main__":
    main()

import time

import spidev

DELAY = 0.5
LDR_CHANNEL = 0

spi = spidev.SpiDev()
spi.open(0, 0)


def readadc(channel):
    if not 0 <= channel <= 7:
        raise ValueError("MCP3008 channel must be between 0 and 7")
    response = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((response[1] & 3) << 8) | response[2]


try:
    spi.max_speed_hz = 100_000
    while True:
        ldr_value = readadc(LDR_CHANNEL)
        print(f"LDR Value: {ldr_value}")
        time.sleep(DELAY)
except KeyboardInterrupt:
    print("\nStopped by User")
finally:
    spi.close()

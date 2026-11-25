import tkinter as tk

import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

root = tk.Tk()
root.title("ADC 전압 측정")
value_label = tk.Label(root, text="ADC 값: -", font=("Helvetica", 18))
value_label.pack(padx=30, pady=(15, 5))
voltage_label = tk.Label(root, text="전압: - V", font=("Helvetica", 18))
voltage_label.pack(pady=5)

job = None


def read_adc():
    global job
    job = None
    try:
        response = spi.xfer2([1, 8 << 4, 0])
    except OSError as error:
        value_label.config(text=f"SPI 오류: {error}")
        toggle_button.config(text="시작")
        return
    value = ((response[1] & 3) << 8) + response[2]
    voltage = value * 3.3 / 1023
    value_label.config(text=f"ADC 값: {value}")
    voltage_label.config(text=f"전압: {voltage:.2f} V")
    job = root.after(500, read_adc)


def stop():
    global job
    if job is not None:
        root.after_cancel(job)
        job = None
    toggle_button.config(text="시작")


def toggle():
    if job is None:
        toggle_button.config(text="정지")
        read_adc()
    else:
        stop()


def close():
    stop()
    spi.close()
    root.destroy()


toggle_button = tk.Button(root, text="시작", width=12, command=toggle)
toggle_button.pack(pady=8)
tk.Button(root, text="종료", width=12, command=close).pack(pady=(0, 12))
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()

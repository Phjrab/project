from flask import Flask
import RPi.GPIO as GPIO


app = Flask(__name__)
LED_PIN = 14


@app.get("/")
def index():
    return '<h1>LED 제어</h1><a href="/on">켜기</a> <a href="/off">끄기</a>'


@app.get("/on", defaults={"state": "on"}, endpoint="led_on")
@app.get("/off", defaults={"state": "off"}, endpoint="led_off")
@app.get("/led/<state>")
def led(state):
    is_on = state == "on"
    GPIO.output(LED_PIN, GPIO.HIGH if is_on else GPIO.LOW)
    return "<h1>LED on</h1>" if is_on else "<h1>LED off</h1>"


@app.get("/led/clean")
def clean():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup(LED_PIN)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    return "<h1>GPIO clean</h1>"


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    try:
        app.run(host="0.0.0.0", port=8080, threaded=False)
    finally:
        GPIO.cleanup(LED_PIN)

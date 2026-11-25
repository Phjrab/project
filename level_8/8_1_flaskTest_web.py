from html import escape

from flask import Flask, abort, redirect, render_template_string, request, url_for


LED_PIN = 14
PORT = 8080

PAGE = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HOME IoT NetWork</title>
</head>
<body>
    <h1>LED On/OFF</h1>
    <form action="{{ url_for('data') }}" method="post">
        <input type="submit" name="led" value="on"{% if not gpio_ready %} disabled{% endif %}>
        <input type="submit" name="led" value="off"{% if not gpio_ready %} disabled{% endif %}>
        <input type="submit" name="led" value="clean">
        <input type="submit" name="led" value="Restart">
    </form>
</body>
</html>
"""


def setup_gpio(gpio):
    gpio.setmode(gpio.BCM)
    gpio.setup(LED_PIN, gpio.OUT, initial=gpio.LOW)


def create_app(gpio):
    app = Flask(__name__)
    gpio_ready = True

    def set_led(enabled):
        if not gpio_ready:
            abort(409, description="Restart를 눌러 GPIO를 다시 설정하세요.")
        gpio.output(LED_PIN, gpio.HIGH if enabled else gpio.LOW)

    def release_gpio():
        nonlocal gpio_ready
        if gpio_ready:
            gpio.output(LED_PIN, gpio.LOW)
            gpio.cleanup(LED_PIN)
            gpio_ready = False

    def restart_gpio():
        nonlocal gpio_ready
        if gpio_ready:
            set_led(False)
        else:
            setup_gpio(gpio)
            gpio_ready = True

    @app.get("/")
    @app.get("/data", endpoint="data")
    def index():
        return render_template_string(PAGE, gpio_ready=gpio_ready)

    @app.post("/data")
    def submit_data():
        command = request.form.get("led")

        if command in ("on", "off"):
            set_led(command == "on")
        elif command == "clean":
            release_gpio()
        elif command == "Restart":
            restart_gpio()
        else:
            abort(400, description="지원하지 않는 LED 명령입니다.")

        return redirect(url_for("data"), code=303)

    @app.get("/on", defaults={"state": "on"}, endpoint="show_on")
    @app.get("/off", defaults={"state": "off"}, endpoint="show_off")
    @app.get("/led/<state>")
    def show_led(state):
        set_led(state == "on")
        return f"<h1>LED {escape(state)}</h1>"

    @app.get("/led/clean")
    def clean():
        release_gpio()
        restart_gpio()
        return "<h1>GPIO clean</h1>"

    @app.post("/led/on")
    def turn_on():
        set_led(True)
        return redirect(url_for("index"), code=303)

    @app.post("/led/off")
    def turn_off():
        set_led(False)
        return redirect(url_for("index"), code=303)

    return app


def main():
    import RPi.GPIO as gpio

    setup_gpio(gpio)
    try:
        create_app(gpio).run(host="0.0.0.0", port=PORT, threaded=False)
    finally:
        if gpio.getmode() is not None and gpio.gpio_function(LED_PIN) == gpio.OUT:
            try:
                gpio.output(LED_PIN, gpio.LOW)
            finally:
                gpio.cleanup(LED_PIN)


if __name__ == "__main__":
    main()

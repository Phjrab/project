from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Flask!"


@app.route("/name")
def name():
    return "<h1>My name is Faker</h1>"


@app.route("/age")
def age():
    return "<h2>My age is 27</h2>"


@app.route("/job")
def job():
    return "<h3>My job is Legend</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

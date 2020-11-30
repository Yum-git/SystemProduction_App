from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    logs = ['20201123 : saoshoahsoa', '20201123 : ahara is xss ']
    return render_template("index.html", logs=logs)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


if __name__ == "__main__":
    app.run(debug=True)
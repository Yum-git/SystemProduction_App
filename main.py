from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    logs = ['20201123 : saoshoahsoa', '20201123 : ahara is xss ']
    return render_template("index.html", logs=logs)


if __name__ == "__main__":
    app.run(debug=True)
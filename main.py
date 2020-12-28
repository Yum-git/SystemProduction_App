from flask import Flask, render_template, request
import crossplane

app = Flask(__name__)


@app.route("/")
def index():
    logs = ['20201123 : saoshoahsoa' for i in range(100)]
    status_all = [['SQL', 'custom'], ['RFI', 'very_hard'], ['TRAVERSAL', 'hard'], ['EVADE', 'soft'], ['XSS', 'very_soft']]

    return render_template("index.html", logs=logs, status_all=status_all)


@app.route("/api", methods=['POST'])
def api():
    print(request.get_data().decode())
    request_data = list(request.get_data().decode().split('='))
    print(request_data)

    print(crossplane.parse('/usr/local/nginx/conf/nginx.conf'))
    return request.form["sql"]


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


if __name__ == "__main__":
    app.run(debug=True)

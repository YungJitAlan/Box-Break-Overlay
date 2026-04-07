from flask import Flask, render_template, request, redirect

app = Flask(__name__)

data = {
    "title": "NFL Prizm Break",
    "pack": 1,
    "last_hit": "None",
    "current_buyer": "TBD",
    "big_hit": "False"
}

@app.route("/")
def overlay():
    return render_template("overlay.html", data=data)

@app.route("/control", methods=["GET", "POST"])
def control():
    if request.method == "POST":
        data["pack"] = request.form.get["pack", data["pack"]]
        data["last_hit"] = request.form.get["last_hit", data["last_hit"]]
        data["current_buyer"] = request.form.get["current_buyer", data["current_buyer"]]
        data["big_hit"] = "big_hit" in request.form
    return render_template("control.html", data=data)

app.run(host="0.0.0.0", port=5000, debug=True)

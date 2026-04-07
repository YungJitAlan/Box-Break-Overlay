from flask import Flask, render_template, request, redirect

app = Flask(__name__)

data = {
    "title": "NBA Prizm Break",
    "pack": 1,
    "last_hit": "None"
}

@app.route("/")
def overlay():
    return render_template("overlay.html", data=data)

@app.route("/control", methods=["GET", "POST"])
def control():
    if request.method == "POST":
        data["pack"] = request.form["pack"]
        data["last_hit"] = request.form["last_hit"]
    return render_template("control.html", data=data)

app.run(debug=True)

from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*" , async_mode='eventlet')

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
        data["pack"] = request.form.get("pack", data["pack"])
        data["last_hit"] = request.form.get("last_hit", data["last_hit"])
        data["current_buyer"] = request.form.get("current_buyer", data["current_buyer"])
        data["big_hit"] = "big_hit" in request.form
        socketio.emit('update', data)
    return render_template("control.html", data=data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

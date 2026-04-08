from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Overlay data
data = {
    "title": "NFL Prizm Break",
    "pack": 1,
    "last_hit": "None",
    "current_buyer": "TBD",
    "big_hit": False
}

# NFL teams
teams = [
    "Patriots","Cowboys","Packers","Chiefs","Seahawks",
    "Ravens","Steelers","Bills","49ers","Bengals",
    "Vikings","Giants","Broncos","Raiders","Rams",
    "Chargers","Eagles","Buccaneers","Titans","Jets",
    "Commanders","Cardinals","Dolphins","Falcons",
    "Panthers","Jaguars","Lions","Browns","Saints",
    "Texans","Colts","Bears"
]

@app.route("/")
def overlay():
    return render_template("overlay.html", data=data, teams=teams)

@app.route("/control", methods=["GET", "POST"])
def control():
    if request.method == "POST":
        data["pack"] = request.form.get("pack", data["pack"])
        data["last_hit"] = request.form.get("last_hit", data["last_hit"])
        data["current_buyer"] = request.form.get("current_buyer", data["current_buyer"])
        data["big_hit"] = "big_hit" in request.form
        socketio.emit('update', data, to='*')  # broadcast to all clients
        data["big_hit"] = False
    return render_template("control.html", data=data)

# Handle team clicks
@socketio.on('team_select')
def handle_team_select(json):
    team = json['team']
    data["current_buyer"] = team
    socketio.emit('update', data, to='*')

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)
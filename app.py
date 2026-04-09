from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

teams = {
    "Patriots": {"buyer": "", "sold": False},
    "Cowboys": {"buyer": "", "sold": False},
    "Packers": {"buyer": "", "sold": False},
    "Chiefs": {"buyer": "", "sold": False},
    "Seahawks": {"buyer": "", "sold": False},
    # add all teams
}

data = {
    "pack": 1,
    "last_hit": "None",
    "big_hit": False
}

def get_remaining():
    return sum(1 for t in teams.values() if not t["sold"])

@app.route("/")
def overlay():
    return render_template("overlay.html", teams=teams, data=data)

@app.route("/control")
def control():
    return render_template("control.html", teams=teams, data=data)

# TEAM CLICK
@socketio.on('select_team')
def select_team(json):
    team = json['team']
    buyer = json['buyer']

    teams[team]["buyer"] = buyer
    teams[team]["sold"] = True

    socketio.emit('update', {
        "teams": teams,
        "data": data,
        "remaining": get_remaining()
    })

# UPDATE GENERAL DATA
@socketio.on('update_data')
def update_data(json):
    data.update(json)

    socketio.emit('update', {
        "teams": teams,
        "data": data,
        "remaining": get_remaining()
    })

# RESET BREAK
@socketio.on('reset')
def reset():
    for t in teams:
        teams[t] = {"buyer": "", "sold": False}

    socketio.emit('update', {
        "teams": teams,
        "data": data,
        "remaining": get_remaining()
    })

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
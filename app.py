#import eventlet
#eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
#socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

DEFAULT_TEAMS = [
    "Cardinals", "Falcons", "Ravens", "Bills", "Panthers", "Bears",
    "Bengals", "Browns", "Cowboys", "Broncos", "Lions", "Packers",
    "Texans", "Colts", "Jaguars", "Chiefs", "Raiders", "Chargers",
    "Rams", "Dolphins", "Vikings", "Patriots", "Saints", "Giants",
    "Jets", "Eagles", "Steelers", "49ers", "Seahawks", "Buccaneers",
    "Titans", "Commanders"
]

teams = {team: {"sold": False, "buyer": ""} for team in DEFAULT_TEAMS}
break_data = {"pack": "", "last_hit": "", "big_hit": False}


def remaining_count():
    return sum(1 for t in teams.values() if not t["sold"])


def broadcast_update():
    socketio.emit("update", {
        "teams": teams,
        "data": break_data,
        "remaining": remaining_count()
    })


@app.route("/")
def controller():
    return render_template("controller.html", teams=teams)


@app.route("/overlay")
def overlay():
    return render_template("overlay.html")


@socketio.on("connect")
def handle_connect():
    emit("update", {
        "teams": teams,
        "data": break_data,
        "remaining": remaining_count()
    })


@socketio.on("select_team")
def handle_select_team(data):
    team = data.get("team")
    buyer = data.get("buyer", "").strip()

    if team in teams and buyer:
        teams[team]["sold"] = True
        teams[team]["buyer"] = buyer
        broadcast_update()


@socketio.on("update_data")
def handle_update_data(data):
    break_data["pack"] = data.get("pack", "")
    break_data["last_hit"] = data.get("last_hit", "")
    break_data["big_hit"] = data.get("big_hit", False)
    broadcast_update()
    break_data["big_hit"] = False


@socketio.on("reset")
def handle_reset():
    global teams, break_data
    teams = {team: {"sold": False, "buyer": ""} for team in DEFAULT_TEAMS}
    break_data = {"pack": "", "last_hit": "", "big_hit": False}
    broadcast_update()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
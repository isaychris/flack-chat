import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel_list = ["lobby"]
online_list = []
online = 0

@app.route("/")
def index():    
    return render_template("lobby.html", online_list=online_list, channel_list=channel_list)

@app.route("/display", )
def display():
    return render_template("lobby.html")

@app.route("/lobby", methods=["GET", "POST"])
def lobby():
    return render_template("lobby.html", online_list=online_list, channel_list=channel_list)


@socketio.on("sent message")
def sent(data):
    print("sent message")
    emit("new message", {"user": data["user"], "time": data["time"], "message": data["message"]}, broadcast=True)

@socketio.on("joined")
def joined(data):
    print(data['display'] + " has joined!")    
    online_list.append(data['display'])
    emit("update online", {"online": len(online_list), "display": data['display'], "event": "joined"}, broadcast=True)

@socketio.on("gone")
def gone(data):
    print(data['display'] + " has left!")
    online_list.remove(data['display'])
    emit("update online", {"online": len(online_list), "display": data['display'], "event": "gone"}, broadcast=True)

@socketio.on("add channel")
def add_channel(data):
    print(data['channel'] + " has been added to channel list!")
    channel_list.append(data['channel'])
    emit("update channels", {"channel": data['channel']}, broadcast=True)
import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel_list = ["lobby"]
online_list = []
messages = {"lobby": []}

@app.route("/")
def index():    
    return redirect(url_for('lobby'))

@app.route("/c/lobby")
def lobby():
    return render_template("channel.html", online_list=online_list, channel_list=channel_list, messages=messages["lobby"], current_channel="lobby")

@app.route("/c/<string:name>")
def channel(name):
    if name not in channel_list:
        return "Error"

    return render_template("channel.html", online_list=online_list, channel_list=channel_list, messages=messages[name], current_channel=name)

@socketio.on("add message")
def sent(data):
    print("message received")
    messages[data["channel"]].append((data["user"], data["time"], data["message"]))
    
    while(len(messages[data["channel"]]) > 100):
        messages[data["channel"]].pop(0)
    
    print(messages[data["channel"]])
    emit("announce message", {"user": data["user"], "time": data["time"], "message": data["message"], "channel": data["channel"] }, broadcast=True)

@socketio.on("add user")
def joined(data):
    print(data['display'] + " has joined!")
    online_list.append(data['display'])
    emit("announce online", {"online": len(online_list), "display": data['display'], "event": "add"}, broadcast=True)

@socketio.on("remove user")
def gone(data):
    print(data['display'] + " has left!")
    online_list.remove(data['display'])
    emit("announce online", {"online": len(online_list), "display": data['display'], "event": "remove"}, broadcast=True)

@socketio.on("add channel")
def add_channel(data):
    print(data['channel'] + " has been added to channel list!")
    channel_list.append(data['channel'])
    messages.setdefault(data['channel'], [])
    emit("announce channel", {"channel": data['channel']}, broadcast=True)
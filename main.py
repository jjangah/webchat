#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/html')
def index():
	nick = "guest_" + str(time.time()).split(".")[0]
	return render_template("main.html", nick_name=nick)


@socketio.on('message')
def handle_message(message):
	socketio.send(message)
	return


@socketio.on('send msg', namespace='/event')
def handle_event_message(message):
	socketio.emit('response', message)
	return

#@socketio.on('connect')
#def connect_message(message):
#	login = "join."	
#	print message
#	if message["login"]:
#		message = message["login"] + " " + login
#	socketio.send(message)
#	return


if __name__ == '__main__':
	app.debug = True
	socketio.run(app)
#	app.run('0.0.0.0')


#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, threading
from flask import Flask, render_template
from flask.ext.socketio import SocketIO
from lib import webchat_lib 

app = Flask(__name__)
socketio = SocketIO(app)
redis_conn = webchat_lib.conn_redis_pubsub()
sub_chat = redis_conn.pubsub()
sub_member = redis_conn.pubsub()

sub_chat.subscribe('chat')
sub_member.subscribe('member')

def listen_chat():
	for m in sub_chat.listen():
		if m['data'] :
			socketio.send(str(m['data']))

try :
	t = threading.Thread(target=listen_chat)
	t.deamon = True
	t.start()
except (KeyboardInterrupt, SystemExit):
	
	raise

except:
	print "KeyboardInterrupted!! exit!" 
	socketio.server.stop()

@app.route('/')
def index():
	nick = "guest_" + str(time.time()).split(".")[0]
	return render_template("main.html", nick_name=nick)

@socketio.on('message')
def handle_message(msg):
	global redis_conn
	new_msg = webchat_lib.trim_msg(msg)	
	redis_conn.publish('chat', new_msg)
	print new_msg	
	return

@socketio.on('connect')
def handle_connect(nick):
	new_nick = webchat_lib.trim_msg(nick)	
	socketio.emit('connect', new_nick)
	return

@socketio.on('disconnect')
def handle_disconnect():
	print "disconnected"
	return

if __name__ == '__main__':
	app.debug = True
	socketio.run(app)

#	app.run('0.0.0.0')


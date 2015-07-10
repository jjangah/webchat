#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, redis, threading, re
from flask import Flask, render_template
from flask.ext.socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

def conn_redis_pubsub():
	r = redis.client.StrictRedis()
	return r

def pub_msg(msg, channel_name):
	global redis_conn
	redis_conn.publish(channel_name, msg)
	print msg
	return

redis_conn = conn_redis_pubsub()
sub_chat = redis_conn.pubsub()
sub_member = redis_conn.pubsub()

sub_chat.subscribe('chat')
sub_member.subscribe('member')

def listen_chat():
	global i
	for m in sub_chat.listen():
		if m['data'] :
			msg = m['data']
			if msg :
				socketio.send(str(msg))

t = threading.Thread(target=listen_chat)
t.deamon = True
t.start()

def trim_msg(msg):
	new_msg = re.sub(r'\n+\t', '', msg)
	return new_msg


@app.route('/')
def index():
	nick = "guest_" + str(time.time()).split(".")[0]
	return render_template("main.html", nick_name=nick)

@socketio.on('message')
def handle_message(msg):
	new_msg = trim_msg(msg)	
	pub_msg(new_msg, 'chat')
	return

@socketio.on('connect')
def handle_connect(nick):
	new_nick = trim_msg(nick)	
	socketio.emit('connect', {"nick":new_nick})
	return


if __name__ == '__main__':
	app.debug = True
	socketio.run(app)
#	app.run('0.0.0.0')



import time
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.send("Hello from client!")

@sio.event
def message(data):
    print("I received a message!", data)

sio.connect('http://chat-server:5000')
sio.wait()

from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    # Using 0.0.0.0 to listen on all available network interfaces inside the container
    socketio.run(app, host='0.0.0.0', port=5000)
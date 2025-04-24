# app.py - Main Flask application
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'voicechat-secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('voice_data')
def handle_voice_data(data):
    # Broadcast the voice data to all clients except sender
    socketio.emit('voice_data', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
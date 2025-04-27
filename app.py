from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('voice_data')
def handle_voice_data(data):
    # Forward the voice data to all other clients
    emit('voice_data', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, server='eventlet')
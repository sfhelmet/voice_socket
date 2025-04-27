from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Store the room password
ROOM_PASSWORD = os.environ.get('ROOM_PASSWORD', 'default-password')
participants = set()

def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('authenticated'):
            return False
        return f(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    if session.get('authenticated'):
        participants.discard(request.sid)
        emit('participant_update', {'count': len(participants)}, broadcast=True)

@socketio.on('leave_room')
def handle_leave_room():
    if session.get('authenticated'):
        participants.discard(request.sid)
        session['authenticated'] = False
        emit('participant_update', {'count': len(participants)}, broadcast=True)

@socketio.on('authenticate')
def handle_authentication(data):
    password = data.get('password')
    
    if not password:
        emit('authentication_failed', {'message': 'Password is required'})
        return
    
    if password != ROOM_PASSWORD:
        emit('authentication_failed', {'message': 'Invalid password'})
        return
    
    session['authenticated'] = True
    participants.add(request.sid)
    emit('authentication_success', {
        'message': 'Successfully joined',
        'participant_count': len(participants)
    })
    emit('participant_update', {'count': len(participants)}, broadcast=True)

@socketio.on('voice_data')
@authenticated_only
def handle_voice_data(data):
    emit('voice_data', data, broadcast=True, include_self=False, binary=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
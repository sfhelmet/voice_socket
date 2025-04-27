from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Store active rooms and their passwords
active_rooms = {}

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

@app.route('/create_room', methods=['POST'])
def create_room():
    room_id = request.form.get('room_id')
    password = request.form.get('password')
    
    if not room_id or not password:
        return {'error': 'Room ID and password are required'}, 400
    
    if room_id in active_rooms:
        return {'error': 'Room already exists'}, 400
    
    active_rooms[room_id] = password
    return {'success': True, 'room_id': room_id}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('authenticate')
def handle_authentication(data):
    room_id = data.get('room_id')
    password = data.get('password')
    
    if not room_id or not password:
        emit('authentication_failed', {'message': 'Room ID and password are required'})
        return
    
    if room_id not in active_rooms:
        emit('authentication_failed', {'message': 'Room does not exist'})
        return
    
    if active_rooms[room_id] != password:
        emit('authentication_failed', {'message': 'Invalid password'})
        return
    
    session['authenticated'] = True
    session['room_id'] = room_id
    join_room(room_id)
    emit('authentication_success', {'message': 'Successfully joined room'})

@socketio.on('voice_data')
@authenticated_only
def handle_voice_data(data):
    room_id = session.get('room_id')
    emit('voice_data', data, room=room_id, include_self=False, binary=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
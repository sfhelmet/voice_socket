# Updated app.py with essential fixes

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Important: Use eventlet as the async mode for better WebRTC support
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, async_mode='eventlet')

# Keep track of users in rooms
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    logger.info(f"Client connected: {request.sid}")
    emit('connect_success', {'message': 'Successfully connected to server'})

@socketio.on('disconnect')
def test_disconnect():
    logger.info(f"Client disconnected: {request.sid}")
    # Remove user from all rooms
    for room_id, user_set in list(rooms.items()):
        if request.sid in user_set:
            user_set.remove(request.sid)
            logger.info(f"Removed disconnected user {request.sid} from room {room_id}")
            room_count = len(rooms.get(room_id, set()))
            
            # Notify others in the room
            emit('user_left', {
                'message': f'A user left room {room_id}',
                'count': room_count
            }, room=room_id)
            
            # Clean up empty rooms
            if not rooms[room_id]:
                del rooms[room_id]

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    
    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(request.sid)
    
    room_count = len(rooms.get(room, set()))
    logger.info(f"User {request.sid} joined room {room}. Users in room: {room_count}")
    
    emit('user_joined', {
        'message': f'A user joined room {room}',
        'count': room_count
    }, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    
    if room in rooms and request.sid in rooms[room]:
        rooms[room].remove(request.sid)
        if not rooms[room]:
            del rooms[room]
    
    room_count = len(rooms.get(room, set()))
    logger.info(f"User {request.sid} left room {room}. Users in room: {room_count}")
    
    emit('user_left', {
        'message': f'A user left room {room}',
        'count': room_count
    }, room=room)

@socketio.on('offer')
def handle_offer(data):
    logger.info(f"Received offer for room {data['room']}")
    # Forward the offer to everyone in the room except the sender
    emit('offer', data, room=data['room'], include_self=False)

@socketio.on('answer')
def handle_answer(data):
    logger.info(f"Received answer for room {data['room']}")
    # Forward the answer to everyone in the room except the sender
    emit('answer', data, room=data['room'], include_self=False)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    logger.info(f"Received ICE candidate for room {data['room']}")
    # Forward the ICE candidate to everyone in the room except the sender
    emit('ice_candidate', data, room=data['room'], include_self=False)

if __name__ == '__main__':
    # Add SSL support for local testing (WebRTC works better with HTTPS)
    if os.path.exists('key.pem') and os.path.exists('cert.pem'):
        socketio.run(app, debug=True, host='0.0.0.0', 
                     keyfile='key.pem', certfile='cert.pem')
    else:
        socketio.run(app, debug=True, host='0.0.0.0')
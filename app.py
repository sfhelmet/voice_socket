# app.py - Streamlit Voice Chat App
import streamlit as st
import socketio
from flask import Flask
from flask_socketio import SocketIO
import eventlet
import threading
import os
import time

# Set page configuration
st.set_page_config(
    page_title="Simple Voice Chat",
    page_icon="🎤",
    layout="centered"
)

# Create a header
st.title("Simple Voice Chat")
st.write("A lightweight voice chat application")

# Initialize session state for connection status
if 'connected' not in st.session_state:
    st.session_state.connected = False
    
if 'server_running' not in st.session_state:
    st.session_state.server_running = False

# Create SocketIO server in a separate thread
def run_socket_server():
    # Create and configure the Flask app
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'voicechat-secret!'
    
    # Configure SocketIO with eventlet
    socket_io = SocketIO(flask_app, async_mode='eventlet', cors_allowed_origins='*')
    
    @socket_io.on('connect')
    def handle_connect():
        print('Client connected')
        
    @socket_io.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
        
    @socket_io.on('voice_data')
    def handle_voice_data(data):
        # Broadcast the voice data to all clients except sender
        socket_io.emit('voice_data', data, broadcast=True, include_self=False)
    
    # Start the server using eventlet
    eventlet.wsgi.server(eventlet.listen(('', 8765)), flask_app)

# Create a start server button
if not st.session_state.server_running:
    if st.button("Start Voice Chat Server"):
        st.session_state.server_running = True
        # Start the SocketIO server in a separate thread
        server_thread = threading.Thread(target=run_socket_server)
        server_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
        server_thread.start()
        st.success("Voice chat server started! Server is running on port 8765.")
        st.experimental_rerun()

# If server is running, show connection panel
if st.session_state.server_running:
    st.success("Voice chat server is running on port 8765.")
    
    # HTML for the voice chat interface
    st.markdown("""
    ## Voice Chat Interface
    Use the controls below to record and send voice messages.
    """)
    
    # Create HTML component with socketio and voice chat interface
    html_code = """
    <div id="status" style="text-align: center; font-weight: bold; margin: 15px 0;">Ready</div>
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <button id="recordButton" style="padding: 10px 20px; margin: 0 10px; font-size: 16px; cursor: pointer;">Start Recording</button>
        <button id="stopButton" style="padding: 10px 20px; margin: 0 10px; font-size: 16px; cursor: pointer;" disabled>Stop Recording</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.1/socket.io.min.js"></script>
    <script>
        // Connect to the Socket.IO server
        const socket = io('http://localhost:8765');
        const recordButton = document.getElementById('recordButton');
        const stopButton = document.getElementById('stopButton');
        const statusElement = document.getElementById('status');

        let mediaRecorder;
        let audioChunks = [];
        let audioContext;
        let isRecording = false;

        // Initialize audio context
        async function initAudio() {
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                
                // Create media recorder
                mediaRecorder = new MediaRecorder(stream);
                
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                    if (mediaRecorder.state === "inactive") {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        
                        // Convert to base64 and send to server
                        const reader = new FileReader();
                        reader.onloadend = () => {
                            const base64data = reader.result.split(',')[1];
                            socket.emit('voice_data', { audio: base64data });
                        };
                        reader.readAsDataURL(audioBlob);
                        audioChunks = [];
                    }
                };

                // Ready to start recording
                recordButton.disabled = false;
                statusElement.textContent = "Ready to chat";
            } catch (err) {
                console.error("Error accessing microphone:", err);
                statusElement.textContent = "Error: " + err.message;
            }
        }

        // Connection status
        socket.on('connect', () => {
            statusElement.textContent = "Connected to server";
            recordButton.disabled = false;
        });

        socket.on('disconnect', () => {
            statusElement.textContent = "Disconnected from server";
            recordButton.disabled = true;
            stopButton.disabled = true;
        });

        // Start recording
        recordButton.onclick = () => {
            if (isRecording) return;
            
            audioChunks = [];
            mediaRecorder.start(1000); // Collect chunks every second
            isRecording = true;
            
            recordButton.disabled = true;
            stopButton.disabled = false;
            statusElement.textContent = "Recording...";
            statusElement.style.color = "red";
        };

        // Stop recording
        stopButton.onclick = () => {
            if (!isRecording) return;
            
            mediaRecorder.stop();
            isRecording = false;
            
            recordButton.disabled = false;
            stopButton.disabled = true;
            statusElement.textContent = "Ready to chat";
            statusElement.style.color = "";
        };

        // Play received audio
        socket.on('voice_data', data => {
            const audio = new Audio("data:audio/webm;base64," + data.audio);
            audio.play();
        });

        // Initialize on page load
        window.onload = initAudio;
    </script>
    """
    
    # Display the HTML component
    st.components.v1.html(html_code, height=200)
    
    # Display connection instructions
    st.markdown("""
    ### Connection Instructions
    
    1. Allow microphone access when prompted
    2. The status indicator will show "Connected to server" when ready
    3. Click "Start Recording" to speak
    4. Click "Stop Recording" when done
    5. Your message will be sent to all other connected users
    
    ### Notes
    
    - Keep this tab open to maintain the connection
    - All users must be connected to the same server
    - For best results, use Chrome or Firefox
    """)
    
    # Add option to stop the server (this is mostly for show in Streamlit)
    if st.button("Stop Server"):
        st.session_state.server_running = False
        st.warning("Attempting to stop the server. You may need to restart the Streamlit app.")
        st.experimental_rerun()

# Add requirements information
st.sidebar.title("App Information")
st.sidebar.markdown("""
### Required Packages
- streamlit
- flask
- flask-socketio
- eventlet
- simple-websocket

### How It Works
This app runs a Flask-SocketIO server in a separate thread while
Streamlit handles the user interface. Voice data is transmitted
between clients using WebSockets.
""")
# Setup and Running Instructions

## Project Structure
First, create the following file structure:
```
voice-chat-app/
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

## Installation
1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
1. Start the Flask application:
   ```
   python app.py
   ```

2. The application will run on `http://127.0.0.1:5000/` by default.

3. Open two different browser windows/tabs and navigate to the URL.

4. In both browser windows:
   - Enter the same room ID (e.g., "room1")
   - Click "Join Room"
   - Once both users have joined, one user should click "Start Audio"
   - Voice communication should now be established between the two browsers

## Testing on Different Devices
If you want to test between different devices on the same network:

1. Modify the `socketio.run()` line in app.py:
   ```python
   socketio.run(app, host='0.0.0.0', debug=True)
   ```

2. Find your computer's local IP address:
   - On Windows: Run `ipconfig` in Command Prompt
   - On macOS/Linux: Run `ifconfig` or `ip addr` in Terminal

3. Access the application from other devices using:
   ```
   http://YOUR_LOCAL_IP:5000/
   ```

4. Note: For security in production, you should not use `host='0.0.0.0'` without proper security measures.

## Troubleshooting
- Ensure your browser has permission to access the microphone
- Some browsers may require HTTPS for WebRTC to work properly
- If testing on different networks, you may need additional TURN servers for WebRTC to work through NATs and firewalls
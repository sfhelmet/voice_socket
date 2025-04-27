# Voice Chat Application

A simple real-time voice chat application built with Flask and WebSocket that allows two users to communicate via voice.

## Features

- Real-time voice communication
- Simple and intuitive interface
- WebSocket-based audio streaming
- Low latency audio processing

## Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd voice-chat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Deployment to Render

1. Push your code to GitHub

2. Go to [Render.com](https://render.com) and:
   - Sign up for a free account
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - Name: voice-chat
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python app.py`
   - Click "Create Web Service"

3. Wait for deployment to complete

## Usage

1. Open the application in two different browser windows
2. Click "Start Chat" in both windows
3. Allow microphone access when prompted
4. Start speaking - the other user will hear you in real-time
5. Click "Stop Chat" when done

## Technical Details

- Built with Flask and Flask-SocketIO
- Uses Web Audio API for real-time audio processing
- WebSocket for low-latency communication
- Base64 encoding for audio data transmission

## Notes

- The free tier of Render will spin down after 15 minutes of inactivity
- First request after inactivity might take 30-60 seconds
- 750 free hours per month included in free tier
# Voice Chat Web App Setup Instructions

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

## Step 1: Setup Project Structure
Create a new directory for your project and set up the basic structure:

```
voice-chat/
├── app.py
└── templates/
    └── index.html
```

## Step 2: Install Dependencies
Open a terminal in your project directory and install the required packages:

```bash
pip install flask flask-socketio
```

## Step 3: Copy the Files
1. Copy the content of the `app.py` file into your project directory.
2. Create a `templates` directory and copy the content of `index.html` into it.

## Step 4: Run the Application
In your terminal, run:

```bash
python app.py
```

The server will start and be accessible at `http://127.0.0.1:5000/` in your web browser.

## Usage Instructions
1. Open the application in your web browser.
2. Allow microphone access when prompted.
3. Click "Start Recording" to begin recording your voice.
4. Click "Stop Recording" when you're done speaking.
5. Your voice message will be sent to all other connected users automatically.

## Notes
- For a real production environment, you'd want to add proper authentication, secure the WebSocket connection, and deploy to a proper server.
- This simple example works best when all users are on the same network or the server is publicly accessible.
- The audio quality is set to basic defaults. For better quality, you could adjust the AudioContext settings.
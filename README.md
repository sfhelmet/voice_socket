# Deployment Instructions

Follow these steps to deploy your Room-Based Chat App to Streamlit:

## 1. Prepare Your Files

Make sure you have these two files:
- `app.py` - The Streamlit application
- `requirements.txt` - Only contains streamlit as a dependency

## 2. Create a GitHub Repository

1. Create a new repository on GitHub
2. Upload both files to the repository
3. Make sure the files are in the root directory

## 3. Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Log in with your GitHub account
3. Click "New app"
4. Select your repository
5. Select the main branch
6. Set the main file path to `app.py`
7. Click "Deploy"

## 4. Share Your App

Once deployed, Streamlit will provide a public URL for your app that you can share with others.

## Important Notes

- This app stores all chat data in session state, which means:
  - Messages are not persistent between sessions
  - Users need to know the exact room ID to join the same room
  - Messages are not synchronized in real-time between different users
  
- To use the app:
  1. Enter any room ID (like "lobby" or "friends")
  2. Users who enter the same room ID will conceptually be in the same room
  3. Each user should set their username for identification
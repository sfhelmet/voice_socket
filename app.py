# app.py - Room-Based Streamlit Chat App
import streamlit as st
from datetime import datetime
import uuid

# Page setup with minimal UI
st.set_page_config(
    page_title="Chat Rooms",
    page_icon="💬",
    layout="centered"
)

# Custom CSS to make the UI cleaner
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .room-header {
        font-size: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'room_joined' not in st.session_state:
    st.session_state.room_joined = False
    
if 'room_id' not in st.session_state:
    st.session_state.room_id = ""
    
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]  # Generate a short user ID
    
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'username' not in st.session_state:
    st.session_state.username = "User-" + st.session_state.user_id

# Functions for handling rooms
def join_room():
    room_id = room_input.strip()
    if room_id:
        st.session_state.room_id = room_id
        st.session_state.room_joined = True
        st.session_state.messages = []  # Clear messages when joining a new room
        return True
    return False
    
def leave_room():
    st.session_state.room_joined = False
    st.session_state.room_id = ""
    st.session_state.messages = []

def send_message(message, message_type="text"):
    if message:
        st.session_state.messages.append({
            "user_id": st.session_state.user_id,
            "username": st.session_state.username,
            "content": message,
            "type": message_type,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

# Main App UI
st.markdown('<div class="main-header">Chat Rooms</div>', unsafe_allow_html=True)

# Room joining interface (shown only when not in a room)
if not st.session_state.room_joined:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        room_input = st.text_input("Enter Room ID:", key="room_id_input", placeholder="Enter any name for your room")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to align with text input
        if st.button("Join Room", use_container_width=True):
            if join_room():
                st.rerun()
                
    with st.expander("Set Username (Optional)"):
        new_username = st.text_input("Your Display Name:", value=st.session_state.username)
        if new_username != st.session_state.username:
            st.session_state.username = new_username
            st.success(f"Username set to: {new_username}")

# Chat interface (shown only when in a room)
else:
    # Room header with leave option
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<div class="room-header">Room: {st.session_state.room_id}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Leave Room", key="leave_room", use_container_width=True):
            leave_room()
            st.rerun()
    
    # Username display
    st.write(f"Chatting as: **{st.session_state.username}**")
    
    # Chat messages area
    st.markdown("### Messages")
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        for msg in st.session_state.messages:
            is_me = msg["user_id"] == st.session_state.user_id
            message_style = "background-color: #EAEAEA; border-radius: 10px; padding: 10px; margin: 5px 0; text-align: left;"
            
            if is_me:
                message_style = "background-color: #DCF8C6; border-radius: 10px; padding: 10px; margin: 5px 0; text-align: right;"
            
            # Message container    
            st.markdown(f"""
            <div style="{message_style}">
                <strong>{"You" if is_me else msg["username"]}</strong> <small>{msg["timestamp"]}</small><br>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Message input area
    user_input = st.text_input("Type a message:", key="msg_input", placeholder="Enter your message here")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Text message input
        if user_input:
            send_message(user_input)
            # Clear input field (requires a rerun)
            st.rerun()
    
    with col2:
        # Voice message option (simplified placeholder)
        if st.button("🎤 Voice", key="voice_btn", use_container_width=True):
            # This would be replaced with actual voice recording functionality
            send_message("🔊 [Voice message]", "voice")
            st.rerun()
    
# Add a small footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 0.8rem;'>Chat Rooms App</div>", unsafe_allow_html=True)
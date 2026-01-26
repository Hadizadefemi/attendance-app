import streamlit as st
import modules.database as db
import time

# --- THIS IS THE FUNCTION YOUR ERROR SAYS IS MISSING ---
def check_login_state():
    """
    Initializes session state variables if they don't exist.
    """
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None

def show_login_screen():
    st.title("🔐 University Attendance Portal")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2995/2995620.png", width=150)
    
    with col2:
        st.markdown("### Log In")
        username = st.text_input("Username", placeholder="e.g., student1")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            user = db.login_user(username, password)
            
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = user
                st.success(f"Welcome back, {user['name']}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Username or Password")

def show_logout_button():
    if st.sidebar.button("🚪 Log Out"):
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None
        st.rerun()
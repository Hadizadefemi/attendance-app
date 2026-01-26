import streamlit as st
from modules import auth, database
from modules import ui_student, ui_lecturers, ui_admin

# --- PAGE SETUP ---
st.set_page_config(page_title="Smart Attendance", page_icon="🎓", layout="centered")

def main():
    # 1. Initialize Session State (Memory)
    # This prevents the app from crashing on first load
    auth.check_login_state()
    
    # 2. CHECK FOR QR SCAN (URL Parameters)
    # If a student scans a QR code, the URL will be: http://.../?session=abc-123
    auth.check_login_state()
    query_params = st.query_params
    
    if "session" in query_params:
        session_id = query_params["session"]
        
        # Save the session ID to memory so we remember it after login
        st.session_state['scanned_session'] = session_id
        
        # Show a notification
        st.toast(f"🔗 Detected Session: {session_id}. Please Log In to mark attendance.", icon="📷")

    # 3. AUTHENTICATION FLOW
    if not st.session_state['logged_in']:
        # If not logged in, show the Login Screen
        auth.show_login_screen()
        
    else:
        # User is logged in!
        user = st.session_state['user_info']
        
        # Show Logout button in the sidebar
        auth.show_logout_button()
        
        # 4. ROUTING (Traffic Control)
        # Decide which dashboard to show based on Role
        if user['role'] == 'Lecturer':
            ui_lecturers.show_dashboard(user)
            
        elif user['role'] == 'Student':
            ui_student.show_dashboard(user)
            
        elif user['role'] == 'Admin':
            ui_admin.show_dashboard(user)
if __name__ == "__main__":
    main()
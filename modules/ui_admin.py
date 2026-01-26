import streamlit as st
import modules.database as db

def show_dashboard(user):
    st.title("🛡️ Admin")
    
    tab1, tab2 = st.tabs(["👥 User Management", "⚙️ System Stats"])
    
    # --- TAB 1: ADD & VIEW USERS ---
    with tab1:
        st.subheader("Add New User")
        st.info("Use this form to register new Students or Lecturers.")
        
        # We use a 'Form' so the page doesn't reload on every keystroke
        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Full Name")
                new_role = st.selectbox("Role", ["Student", "Lecturer", "Admin"])
            with col2:
                new_user = st.text_input("Username")
                new_pass = st.text_input("Default Password", type="password")
            
            submitted = st.form_submit_button("Create Account")
            
            if submitted:
                if new_name and new_user and new_pass:
                    success, msg = db.add_user(new_user, new_pass, new_name, new_role)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill in all fields.")

        st.markdown("---")
        st.subheader("Current Database Users")
        all_users = db.get_all_users()
        st.dataframe(all_users, use_container_width=True)

    # --- TAB 2: SYSTEM STATS ---
    with tab2:
        st.subheader("System Health")
        
        # Calculate some basic totals
        users = db.load_data(db.USERS_FILE)
        sessions = db.load_data(db.SESSIONS_FILE)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(users))
        col2.metric("Classes Held", len(sessions))
        col3.metric("System Status", "Online", delta="OK")
import streamlit as st
import modules.database as db
import time

def show_dashboard(user):
    st.title(f"🎓 Student Portal: {user['name']}")
    
    # --- PART 1: AUTO-MARK ATTENDANCE ---
    # Check if the user came here by scanning a QR code
    if 'scanned_session' in st.session_state and st.session_state['scanned_session']:
        session_id = st.session_state['scanned_session']
        
        with st.status("Processing QR Code...", expanded=True):
            time.sleep(1) # Visual effect
            success, message = db.mark_attendance(user['username'], session_id)
            
            if success:
                st.success(message)
                
            else:
                st.warning(message)
        
        # Clear the scan so it doesn't try to mark again on reload
        st.session_state['scanned_session'] = None

        # forces the browser URL to clear the "?session=..." part
        st.query_params.clear()

        time.sleep(2)
        st.rerun()

    # --- PART 2: ATTENDANCE ANALYTICS ---
    st.markdown("### 📊 My Attendance Status")
    
    # Get the calculated stats (including the %)
    stats = db.get_student_stats(user['username'])
    
    if stats.empty:
        st.info("No class sessions recorded yet.")
    else:
        # Display each course as a "Card"
        for index, row in stats.iterrows():
            course = row['course_code']
            perc = row['percentage']
            attended = int(row['attended_sessions'])
            total = int(row['total_sessions'])
            
            # Create a visual container for the course
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"{course}")
                    st.write(f"Attended: **{attended}/{total}** classes")
                    
                    # Progress Bar logic
                    bar_color = "green" if perc >= 75 else "red"
                    st.progress(perc / 100)
                    
                    if perc < 75:
                        st.error(f"⚠️ Warning: You are at {perc}%. You need 75% for exams!")
                    else:
                        st.success(f"✅ Safe! ({perc}%)")
                
                with col2:
                    # Big number display
                    st.metric(label="Attendance", value=f"{perc}%")
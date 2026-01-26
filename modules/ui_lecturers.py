import streamlit as st
import modules.database as db
import qrcode
from io import BytesIO

PERMANENT_URL = "https://attendance-app-8dkqufve4pz4ryxbz9xvga.streamlit.app/"

def generate_qr_image(url):
    """Generates a QR code image from a URL string."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for Streamlit
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def show_dashboard(user):
    st.title(f"👨‍🏫 Lecturer Portal: {user['name']}")
    
    # Tabs to organize the view
    tab1, tab2 = st.tabs(["📷 Start Class (QR)", "📋 Class History"])
    
    # --- TAB 1: GENERATE SESSION ---
    with tab1:
        st.subheader("Start a New Class Session")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            course_code = st.selectbox("Select Course", ["MAT312", "PHY101", "CSC202"])
        
        with col2:
            # TEACHER MUST ENTER THEIR IP ADDRESS HERE
            # To find it: Open CMD -> type 'ipconfig' -> look for IPv4 Address
            st.info(f"Linking to: {PERMANENT_URL}")

        if st.button("Generate Attendance QR", type="primary"):
            # 1. Create Session
            session_id = db.create_session(course_code, user['username'])
            
            # 2. Use the Hardcoded Link automatically
            clean_url = PERMANENT_URL.rstrip("/") 
            link = f"{clean_url}/?session={session_id}"
            
            # 3. Generate Image
            qr_img = generate_qr_image(link)
            
            # 4. Show Result
            st.success(f"Session Active! ID: {session_id}")
            st.image(qr_img, caption=f"Scan to attend {course_code}", width=350)
            

    # --- TAB 2: HISTORY & REPORTS ---
    with tab2:
        st.subheader("📋 Class Attendance Reports")
        
        # 1. Get all classes taught by this teacher
        my_sessions = db.get_lecturer_sessions(user['username'])
        
        if my_sessions.empty:
            st.info("You haven't created any class sessions yet.")
        else:
            # 2. Create a Dropdown to pick a class
            # We display "Course - Date (ID)" to make it readable
            session_options = my_sessions.apply(
                lambda x: f"{x['course_code']} - {x['date']} ({x['session_id']})", axis=1
            )
            
            selected_option = st.selectbox("Select a Past Class", session_options)
            
            # Extract the actual session_id from the text string
            # Example: "MAT312 - 2026-01-25 (abc-123)" -> we want "abc-123"
            selected_session_id = selected_option.split("(")[-1].replace(")", "")
            
            # 3. Fetch and Display Data
            st.markdown("---")
            attendance_list = db.get_session_attendance_list(selected_session_id)
            
            if attendance_list.empty:
                st.warning("No students have scanned in for this class yet.")
            else:
                count = len(attendance_list)
                st.metric("Total Present", f"{count} Students")
                
                # Show the nice table
                st.dataframe(
                    attendance_list, 
                    use_container_width=True,
                    hide_index=True # Hides the 0, 1, 2 row numbers
                )
                
                # Bonus: Download Button
                csv = attendance_list.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Attendance CSV",
                    data=csv,
                    file_name=f"attendance_{selected_session_id}.csv",
                    mime="text/csv"

                )

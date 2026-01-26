import pandas as pd
import os
import uuid
from datetime import datetime

# --- CONFIGURATION ---
USERS_FILE = "data/users.csv"
SESSIONS_FILE = "data/sessions.csv"
ATTENDANCE_FILE = "data/attendance.csv"

def load_data(filepath):
    """
    Safely reads a CSV. Returns an empty DataFrame if file is missing or empty.
    """
    # 1. Check if file exists
    if not os.path.exists(filepath):
        return pd.DataFrame()
    
    # 2. Check if file is empty (0 bytes)
    if os.path.getsize(filepath) == 0:
        return pd.DataFrame()

    try:
        # 3. CRITICAL: The 'return' keyword must be here!
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame()

# ==========================================
# 1. USER MANAGEMENT
# ==========================================

def login_user(username, password):
    df = load_data(USERS_FILE)
    
    # SAFETY CHECK: If df is empty, no one can log in
    if df.empty:
        return None
    
    user = df[(df['username'] == username) & (df['password'] == password)]
    
    if not user.empty:
        return user.iloc[0].to_dict()
    return None

# ==========================================
# 2. LECTURER FEATURES
# ==========================================

def create_session(course_code, teacher_username):
    df = load_data(SESSIONS_FILE)
    
    session_id = str(uuid.uuid4())[:8]
    today = datetime.now().strftime("%Y-%m-%d")
    
    new_session = pd.DataFrame([{
        "session_id": session_id,
        "course_code": course_code,
        "date": today,
        "created_by": teacher_username
    }])
    
    df = pd.concat([df, new_session], ignore_index=True)
    df.to_csv(SESSIONS_FILE, index=False)
    return session_id

# ==========================================
# 3. STUDENT FEATURES
# ==========================================

def mark_attendance(student_username, session_id):
    df = load_data(ATTENDANCE_FILE)
    
    # Check if already attended
    if not df.empty:
        existing = df[(df['student_username'] == student_username) & 
                      (df['session_id'] == session_id)]
        if not existing.empty:
            return False, "You have already marked attendance for this class."
    
    new_entry = pd.DataFrame([{
        "session_id": session_id,
        "student_username": student_username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(ATTENDANCE_FILE, index=False)
    return True, "Attendance Marked Successfully!"

def get_student_stats(student_username):
    """Calculates attendance percentage."""
    sessions = load_data(SESSIONS_FILE)
    attendance = load_data(ATTENDANCE_FILE)
    
    # SAFETY CHECK: If we can't load sessions, return empty table immediately
    if sessions.empty:
        return pd.DataFrame()

    # 1. Count Total Classes
    total_classes = sessions.groupby("course_code").size().reset_index(name="total_sessions")
    
    # 2. If student has ZERO attendance, just return the totals with 0%
    if attendance.empty:
        total_classes['attended_sessions'] = 0
        total_classes['percentage'] = 0.0
        return total_classes

    # 3. Calculate Stats
    my_attendance = attendance[attendance['student_username'] == student_username]
    valid_attendance = pd.merge(my_attendance, sessions, on="session_id")
    attended_counts = valid_attendance.groupby("course_code").size().reset_index(name="attended_sessions")
    
    stats = pd.merge(total_classes, attended_counts, on="course_code", how="left")
    stats = stats.fillna(0)
    
    stats['percentage'] = (stats['attended_sessions'] / stats['total_sessions']) * 100
    stats['percentage'] = stats['percentage'].round(1)
    
    return stats

# ==========================================
# 4. REPORTING TOOLS
# ==========================================

def get_lecturer_sessions(lecturer_username):
    """Returns all sessions created by a specific teacher."""
    df = load_data(SESSIONS_FILE)
    if df.empty:
        return pd.DataFrame()
    # Filter: Show newest classes first
    return df[df['created_by'] == lecturer_username].sort_values(by='date', ascending=False)

def get_session_attendance_list(session_id):
    """Returns the names and times of students who attended a specific session."""
    att = load_data(ATTENDANCE_FILE)
    users = load_data(USERS_FILE)
    
    if att.empty:
        return pd.DataFrame()
        
    # 1. Filter attendance for just this session
    relevant_attendance = att[att['session_id'] == session_id]
    
    if relevant_attendance.empty:
        return pd.DataFrame()

    # 2. Merge to get Real Names (instead of just usernames)
    # We match 'student_username' from attendance to 'username' in users
    merged = pd.merge(relevant_attendance, users, left_on='student_username', right_on='username')
    
    # 3. Clean up the table (Select only what we want to see)
    clean_view = merged[['name', 'student_username', 'timestamp']]
    clean_view.columns = ["Student Name", "ID", "Time Scanned"] # Rename headers for the UI
    
    return clean_view


# ==========================================
# 5. ADMIN TOOLS
# ==========================================

def get_all_users():
    """Returns a list of all users (for the Admin view)."""
    df = load_data(USERS_FILE)
    if df.empty:
        return pd.DataFrame()
    # Return everything except the password for security
    return df[['name', 'username', 'role']]

def add_user(username, password, name, role):
    """
    Adds a new user to the database.
    Returns: (True, Success Message) or (False, Error Message)
    """
    df = load_data(USERS_FILE)
    
    # 1. Check if username exists
    if not df.empty and username in df['username'].values:
        return False, "Error: Username already exists!"
    
    # 2. Add new row
    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "name": name,
        "role": role
    }])
    
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)
    return True, f"Successfully added {role}: {name}"
import pandas as pd
import os

# Define the folder where data will live
DATA_FOLDER = "data"

# 1. Create the folder if it doesn't exist
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def create_dummy_data():
    # --- TABLE 1: USERS ---
    # We are creating a Lecturer (Dr. Smith) and a Student (John Doe)
    users_data = {
        "username": ["admin", "student1", "student2", "prof_smith"],
        "password": ["1234", "1234", "1234", "pass"], # Simple passwords for testing
        "name": ["Admin User", "John Doe", "Jane Smith", "Dr. Alistair Smith"],
        "role": ["Admin", "Student", "Student", "Lecturer"]
    }
    df_users = pd.DataFrame(users_data)
    df_users.to_csv(f"{DATA_FOLDER}/users.csv", index=False)
    print(f"✅ Created {DATA_FOLDER}/users.csv")

    # --- TABLE 2: SESSIONS (Classes that happened) ---
    # We pretend 3 Math classes and 1 Physics class already happened
    sessions_data = {
        "session_id": ["MATH_01", "MATH_02", "MATH_03", "PHY_01"],
        "course_code": ["MAT312", "MAT312", "MAT312", "PHY101"],
        "date": ["2026-01-10", "2026-01-12", "2026-01-14", "2026-01-10"],
        "created_by": ["prof_smith", "prof_smith", "prof_smith", "prof_smith"]
    }
    df_sessions = pd.DataFrame(sessions_data)
    df_sessions.to_csv(f"{DATA_FOLDER}/sessions.csv", index=False)
    print(f"✅ Created {DATA_FOLDER}/sessions.csv")

    # --- TABLE 3: ATTENDANCE LOG (Who was there) ---
    # John (student1) attended 2 out of the 3 Math classes
    attendance_data = {
        "session_id": ["MATH_01", "MATH_02"],
        "student_username": ["student1", "student1"],
        "timestamp": ["2026-01-10 10:05:00", "2026-01-12 10:01:00"]
    }
    df_attendance = pd.DataFrame(attendance_data)
    df_attendance.to_csv(f"{DATA_FOLDER}/attendance.csv", index=False)
    print(f"✅ Created {DATA_FOLDER}/attendance.csv")

if __name__ == "__main__":
    create_dummy_data()
    print("\n🎉 Database setup complete! Check your 'data' folder.")
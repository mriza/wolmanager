import sqlite3
import getpass
from werkzeug.security import generate_password_hash

def get_db_connection():
    """Establish a database connection."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_user():
    """Interactive CLI to add a new user to the database."""
    print("\n=== Add New User ===")
    full_name = input("Full Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    username = input("Username: ")
    
    while True:
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password == confirm_password:
            break
        print("Passwords do not match. Try again.")
    
    password_hash = generate_password_hash(password)
    role = input("Role (admin/user): ").strip().lower()
    if role not in ["admin", "user"]:
        print("Invalid role. Defaulting to 'user'.")
        role = "user"
    
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO users (full_name, email, phone, username, password, role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (full_name, email, phone, username, password_hash, role))
        conn.commit()
        print("\n✅ User added successfully!")
    except sqlite3.IntegrityError:
        print("\n❌ Error: Username already exists!")
    finally:
        conn.close()

if __name__ == "__main__":
    add_user()

import sqlite3

def update_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_database()
    print("Database updated successfully.")

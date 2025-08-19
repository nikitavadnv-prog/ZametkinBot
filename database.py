import sqlite3

def init_db():
    conn = sqlite3.connect("trainings.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_chat_id INTEGER,
            training_datetime TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_training(client_name, client_chat_id, training_datetime):
    conn = sqlite3.connect("trainings.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trainings (client_name, client_chat_id, training_datetime)
        VALUES (?, ?, ?)
    """, (client_name, client_chat_id, training_datetime))
    conn.commit()
    conn.close()

def get_upcoming_trainings():
    conn = sqlite3.connect("trainings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trainings")
    rows = cursor.fetchall()
    conn.close()
    return rows

import sqlite3

def create_database_and_table():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('q3ai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ifp (
            ask_date DATE,
            active_state TEXT,
            resolution REAL,
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            background TEXT,
            fine_print TEXT,
            resolution_criteria TEXT,
            json TEXT
        )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__=="__main__":
    create_database_and_table()
import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect("solar_reports.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            file_path TEXT,
            date_created TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert a new file record
def insert_file(filename, file_path):
    conn = sqlite3.connect("solar_reports.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (filename, file_path, date_created) VALUES (?, ?, datetime('now'))",
                   (filename, file_path))
    conn.commit()
    conn.close()

# Fetch saved reports
def get_saved_files():
    conn = sqlite3.connect("solar_reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT filename, file_path, date_created FROM reports ORDER BY date_created DESC")
    files = cursor.fetchall()
    conn.close()
    return files
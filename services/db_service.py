import sqlite3
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

def init_db():
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    
def get_db_connection():
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    conn.row_factory = sqlite3.Row
    return conn
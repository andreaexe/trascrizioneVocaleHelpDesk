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
    
    # Tabella per memorizzare le trascrizioni
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            transcript TEXT NOT NULL,
            segments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES audio_files (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
def get_db_connection():
    conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
    conn.row_factory = sqlite3.Row
    return conn
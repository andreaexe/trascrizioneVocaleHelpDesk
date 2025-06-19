from services.db_service import get_db_connection

class AudioFile:
    @staticmethod
    def save_to_db(filename, original_filename, file_path):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audio_files (filename, original_filename, file_path) VALUES (?, ?, ?)",
            (filename, original_filename, file_path)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audio_files ORDER BY upload_date DESC")
        audio_files = cursor.fetchall()
        conn.close()
        return audio_files
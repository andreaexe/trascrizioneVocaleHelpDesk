from services.db_service import get_db_connection
import sqlite3
from services.transcription_service import transcribe_with_openai

class AudioFile:
    @staticmethod
    def save_to_db(filename, original_filename, file_path):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audio_files (filename, original_filename, file_path) VALUES (?, ?, ?)",
            (filename, original_filename, file_path)
        )
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audio_files ORDER BY upload_date DESC")
        audio_files = cursor.fetchall()
        conn.close()
        return audio_files
        
    @staticmethod
    def get_by_id(file_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audio_files WHERE id = ?", (file_id,))
        audio_file = cursor.fetchone()
        conn.close()
        return audio_file
    
    @staticmethod
    def transcribe_audio(file_path, language=None):
        """Trascrive un file audio utilizzando l'API OpenAI Whisper"""
        try:
            transcription = transcribe_with_openai(file_path, language)
            return transcription
        except Exception as e:
            # In caso di errore, restituisce un dizionario con l'errore
            return {"error": str(e)}
    
    @staticmethod
    def save_transcription(file_id, transcription):
        """Salva la trascrizione nel database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Controlliamo se esiste già una trascrizione per questo file
            cursor.execute("SELECT id FROM transcriptions WHERE file_id = ?", (file_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Aggiorna la trascrizione esistente
                cursor.execute(
                    "UPDATE transcriptions SET transcript = ?, segments = ? WHERE file_id = ?",
                    (transcription["transcript"], str(transcription["segments"]), file_id)
                )
            else:
                # Inserisce una nuova trascrizione
                cursor.execute(
                    "INSERT INTO transcriptions (file_id, transcript, segments) VALUES (?, ?, ?)",
                    (file_id, transcription["transcript"], str(transcription["segments"]))
                )
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Errore database: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_transcription(file_id):
        """Recupera la trascrizione per un file audio"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transcriptions WHERE file_id = ?", (file_id,))
        transcription = cursor.fetchone()
        conn.close()
        return transcription
from flask import Flask, jsonify
from controllers.audio_controller import home, mostra_richieste
from services.db_service import init_db
from models.audio import AudioFile
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

# Inizializza il database al primo avvio
init_db()

# Definizione delle route
@app.route("/", methods=["GET", "POST"])
def index():
    return home()

@app.route("/richieste")
def richieste():
    return mostra_richieste()

@app.route("/transcribe/<int:file_id>", methods=["POST"])
def transcribe(file_id):
    """Trascrive manualmente un file audio già caricato"""
    audio_file = AudioFile.get_by_id(file_id)
    
    if not audio_file:
        return jsonify({"success": False, "error": "File non trovato"}), 404
    
    try:
        # Trascrivi il file
        file_path = audio_file['file_path']
        transcription = AudioFile.transcribe_audio(file_path)
        
        # Salva la trascrizione nel database
        if 'error' not in transcription:
            AudioFile.save_transcription(file_id, transcription)
            return jsonify({
                "success": True, 
                "transcript": transcription["transcript"]
            })
        else:
            return jsonify({
                "success": False, 
                "error": transcription["error"]
            }), 500
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

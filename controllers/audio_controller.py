import os
from flask import request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from models.audio import AudioFile
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni le variabili d'ambiente
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/audio')
# Gestione più robusta per ALLOWED_EXTENSIONS
allowed_ext = os.getenv('ALLOWED_EXTENSIONS')
ALLOWED_EXTENSIONS = allowed_ext.split(',') if allowed_ext else ['mp3', 'wav', 'ogg', 'm4a']

def allowed_file(filename):
    """Controlla se il file ha un'estensione consentita"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def home():
    """Gestisce la homepage con il form di upload"""
    message = None
    if request.method == "POST":
        # Check se è stato caricato un file
        if 'audio_file' not in request.files:
            message = "Nessun file selezionato"
        else:
            file = request.files['audio_file']
            # Se l'utente non seleziona un file, il browser invia un file senza nome
            if file.filename == '':
                message = "Nessun file selezionato"
            # Se il file esiste e ha un'estensione consentita
            elif file and allowed_file(file.filename):
                # Sicurezza: sanitizza il nome del file
                original_filename = file.filename
                filename = secure_filename(file.filename)                # Salva il file nel filesystem
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Salva le informazioni del file nel database tramite il modello
                file_id = AudioFile.save_to_db(filename, original_filename, file_path)
                
                # Esegui la trascrizione del file audio
                try:
                    # Determina la lingua (opzionale, usa null per l'autodetect)
                    language = request.form.get('language', None)
                    
                    # Trascrivi il file
                    transcription = AudioFile.transcribe_audio(file_path, language)
                    
                    # Salva la trascrizione nel database
                    if 'error' not in transcription:
                        AudioFile.save_transcription(file_id, transcription)
                        message = f"File {original_filename} caricato e trascritto con successo!"
                    else:
                        message = f"File caricato, ma si è verificato un errore nella trascrizione: {transcription['error']}"
                except Exception as e:
                    message = f"File caricato, ma si è verificato un errore durante la trascrizione: {str(e)}"
                
                # Reindirizza alla pagina delle richieste
                return redirect(url_for('richieste'))
            else:
                message = "Formato file non supportato. Usa .mp3, .wav, .ogg o .m4a"
                
    return render_template("home.html", message=message)
    
def mostra_richieste():
    """Mostra tutte le richieste audio caricate"""
    # Recupera tutti i file audio dal database tramite il modello
    audio_files = AudioFile.get_all()
    
    # Per ogni file, controlla se esiste una trascrizione
    for audio in audio_files:
        transcription = AudioFile.get_transcription(audio['id'])
        if transcription:
            audio['has_transcription'] = True
            audio['transcript'] = transcription['transcript']
        else:
            audio['has_transcription'] = False
    
    return render_template("richieste.html", audio_files=audio_files)

# Funzione per eseguire la trascrizione manualmente
def transcribe_audio(file_id):
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
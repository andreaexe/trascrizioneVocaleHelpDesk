import os
from flask import request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from models.audio import AudioFile
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni le variabili d'ambiente
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(',')

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
                filename = secure_filename(file.filename)
                # Salva il file nel filesystem
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                  # Salva le informazioni del file nel database tramite il modello
                AudioFile.save_to_db(filename, original_filename, file_path)
                
                message = f"File {original_filename} caricato con successo!"
                # Reindirizza alla pagina delle richieste
                return redirect(url_for('richieste'))
            else:
                message = "Formato file non supportato. Usa .mp3, .wav, .ogg o .m4a"
                
    return render_template("home.html", message=message)
    
def mostra_richieste():
    """Mostra tutte le richieste audio caricate"""
    # Recupera tutti i file audio dal database tramite il modello
    audio_files = AudioFile.get_all()
    
    return render_template("richieste.html", audio_files=audio_files)
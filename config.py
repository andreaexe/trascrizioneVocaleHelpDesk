import os

# Configurazione per l'upload dei file
UPLOAD_FOLDER = 'static/audio'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a'}
DATABASE_PATH = 'helpdesk.db'

# Assicurarsi che la cartella per l'upload esista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
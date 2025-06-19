from flask import Flask
from controllers.audio_controller import home, mostra_richieste
from services.db_service import init_db
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inizializza il database al primo avvio
init_db()

# Definizione delle route
@app.route("/", methods=["GET", "POST"])
def index():
    return home()

@app.route("/richieste")
def richieste():
    return mostra_richieste()

if __name__ == "__main__":
    app.run(debug=True)

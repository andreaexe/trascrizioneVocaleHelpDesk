# Help Desk - Sistema gestione chiamate

Sistema di gestione chiamate per help desk che permette di:
- Caricare file audio di richieste
- Visualizzare l'elenco delle richieste audio
- (Future) Trascrizione automatica delle richieste vocali
- (Future) Generazione PDF organizzati delle richieste

## Installazione

1. Clonare il repository
2. Creare un ambiente virtuale: `python -m venv .venv`
3. Attivare l'ambiente virtuale:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
4. Installare le dipendenze: `pip install -r requirements.txt`
5. Configurare le variabili d'ambiente:
   - Copiare il file `.env.example` in un nuovo file chiamato `.env`
   - Modificare i valori nel file `.env` in base alle proprie esigenze

## Esecuzione

L'applicazione sarà disponibile all'indirizzo `http://127.0.0.1:5000/`

## Struttura del progetto

- `app.py`: Entry point dell'applicazione
- `controllers/`: Gestione delle richieste HTTP
- `models/`: Modelli di dati e interazione con il database
- `services/`: Servizi condivisi
- `static/`: File statici (CSS, JS, audio)
- `templates/`: Template HTML
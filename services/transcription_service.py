import os
import requests
from pathlib import Path
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def transcribe_with_openai(audio_path, language=None):
    """
    Trascrive un file audio utilizzando l'API OpenAI Whisper
    """
    if not OPENAI_API_KEY:
        raise ValueError("API key di OpenAI non impostata. Imposta OPENAI_API_KEY nelle variabili d'ambiente.")
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    # Prepara i parametri per l'API
    params = {}
    if language and language != "auto":
        params["language"] = language
    
    # Invia la richiesta all'API OpenAI
    with open(audio_path, 'rb') as audio_file:
        files = {
            'file': (Path(audio_path).name, audio_file, 'audio/mpeg'),
            'model': (None, 'whisper-1'),
        }
        
        for key, value in params.items():
            files[key] = (None, value)
        
        response = requests.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers=headers,
            files=files
        )
    
    if response.status_code != 200:
        error_message = f"Errore API: {response.status_code} - {response.text}"
        logger.error(error_message)
        raise Exception(error_message)
    
    result = response.json()
    
    # Formatta la risposta per essere compatibile con l'interfaccia frontend
    formatted_response = {
        "transcript": result.get("text", ""),
        "confidence": 0.9,  # OpenAI non fornisce un valore di confidenza, usiamo un valore predefinito alto
        "segments": []
    }
    
    # Simula i segmenti per supportare i timestamp nel frontend
    words = formatted_response["transcript"].split()
    words_per_segment = 15
    segments = []
    
    for i in range(0, len(words), words_per_segment):
        segment_words = words[i:i+words_per_segment]
        segment_text = " ".join(segment_words)
        start_time = (i / len(words)) * (len(words) / 20)  # Simula un tempo di circa 20 parole al secondo
        end_time = start_time + (len(segment_words) / 20)
        
        segments.append({
            "start": start_time,
            "end": end_time,
            "text": segment_text
        })
    
    formatted_response["segments"] = segments
    return formatted_response

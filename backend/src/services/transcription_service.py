import os
import tempfile
from openai import OpenAI
from config import Config

# OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)


def transcribe_audio_file(audio_file):
    """
    Receives an uploaded audio file (Flask FileStorage)
    Saves temporarily, sends to Whisper, returns text
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="he"
            )

        return transcript.text

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
import os
from gtts import gTTS
from config import UPLOAD_FOLDER

def generate_audio(summary_text):
    audio_path = os.path.join(UPLOAD_FOLDER, "audio_summary.mp3")
    tts = gTTS(summary_text, lang="en")
    tts.save(audio_path)
    return audio_path

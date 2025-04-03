import speech_recognition as sr
from elevenlabs import ElevenLabs
from config import ELEVENLABS_API_KEY
import tempfile
import os
from pydub import AudioSegment
from pydub.playback import play as play_audio

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def listen_from_vbcable():
    r = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    mic_index = next((i for i, name in enumerate(mics) if "CABLE Output" in name), None)

    if mic_index is None:
        raise Exception("❌ VB-CABLE Output device not found.")

    with sr.Microphone(device_index=mic_index) as source:
        print("🎤 Listening from CABLE Output...")
        audio = r.listen(source)
        return audio

def transcribe(audio):
    r = sr.Recognizer()
    try:
        return r.recognize_whisper(audio)
    except sr.UnknownValueError:
        return "[Could not understand]"
    except Exception as e:
        return f"[Error: {e}]"

def speak(text):
    print("🗣 AI Speaking:", text)
    response_stream = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )

    # Save streamed MP3 response to a file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        for chunk in response_stream:
            f.write(chunk)
        audio_path = f.name

    # Convert MP3 to WAV and play it (for better compatibility)
    audio = AudioSegment.from_file(audio_path, format="mp3")
    play_audio(audio)

    os.remove(audio_path)

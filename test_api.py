import requests
from config import HUGGINGFACE_API_KEY, ELEVENLABS_API_KEY
from elevenlabs.client import ElevenLabs
import pyttsx3
from zoom_integration import create_meeting

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def test_huggingface_llm():
    try:
        prompt = "Generate 3 interview questions for a backend engineer skilled in Python and Django."
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 150, "temperature": 0.7}
        }
        res = requests.post(HF_API_URL, headers=HEADERS, json=payload)
        if res.status_code == 200:
            print("✅ Hugging Face LLM Test Successful:")
            print(res.json()[0]["generated_text"].strip())
        else:
            print("❌ Hugging Face LLM Error:", res.status_code, res.text)
    except Exception as e:
        print("❌ Exception during Hugging Face LLM Test:", str(e))

# Keep ElevenLabs and Zoom tests as they are


# Test 2: ElevenLabs API (with pyttsx3 fallback)
def test_elevenlabs():
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text="This is a test of ElevenLabs text-to-speech.",
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        with open("test_audio.mp3", "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print("ElevenLabs Test Successful: Audio generated and saved as test_audio.mp3.")
    except Exception as e:
        print("ElevenLabs Test Failed:")
        print(str(e))
        print("Falling back to pyttsx3...")
        try:
            engine = pyttsx3.init()
            engine.say("This is a test of pyttsx3 text-to-speech.")
            engine.runAndWait()
            print("pyttsx3 Test Successful: Audio played.")
        except Exception as fallback_e:
            print("pyttsx3 Test Failed:")
            print(str(fallback_e))

# Test 3: Zoom API (Server-to-Server OAuth)
def test_zoom():
    try:
        meeting_url = create_meeting()
        if meeting_url:
            print("Zoom Test Successful: Meeting created.")
            print(f"Meeting URL: {meeting_url}")
        else:
            print("Zoom Test Failed: Could not create meeting.")
    except Exception as e:
        print("Zoom Test Failed:")
        print(str(e))


# Run all tests
if __name__ == "__main__":
    print("=== Testing OpenAI API ===")
    test_huggingface_llm()
    print("\n=== Testing ElevenLabs API ===")
    test_elevenlabs()
    print("\n=== Testing Zoom API ===")
    test_zoom()
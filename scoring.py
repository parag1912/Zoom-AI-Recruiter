# scoring.py
import requests
from config import HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def score_interview(transcript):
    prompt = f"""
You are an AI interviewer. Read the candidate's answers and give a score from 1 to 10 along with one paragraph of feedback.

Candidate Transcript:
{transcript}

Respond in this format:
Score: X/10
Feedback: <your feedback here>
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.5,
            "return_full_text": False
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload)
    if res.status_code == 200:
        output = res.json()
        return output[0]["generated_text"].strip()
    else:
        print("❌ Scoring API Error:", res.status_code, res.text)
        return "Error: Could not score interview"

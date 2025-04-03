import requests
from config import HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def generate_questions(skills):
    prompt = f"""
    Based on the following job description or skills:
    {skills}

    Generate 3 concise interview questions (mix of technical and behavioral).
    """
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=data)
    if res.status_code == 200:
        return res.json()[0]["generated_text"].strip()
    else:
        print("❌ Question Generator Error:", res.status_code, res.text)
        return "Error: Failed to generate questions"

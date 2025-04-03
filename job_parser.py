# job_parser.py
import requests
from config import HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def extract_skills_and_responsibilities(jd):
    prompt = f"""
    Extract 5 important technical skills and 3 key responsibilities from this job description:
    {jd}
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.3,
            "return_full_text": False
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json()[0]["generated_text"].strip()
    else:
        print("❌ Job Parser Error:", res.status_code, res.text)
        return "Error: Failed to extract skills and responsibilities"

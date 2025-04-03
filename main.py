# main.py
from job_parser import extract_skills_and_responsibilities
from question_generator import generate_questions
from voice_interface import speak, listen_from_vbcable, transcribe
from zoom_integration import create_meeting
from scoring import score_interview
import requests
from config import HUGGINGFACE_API_KEY
import time
import re

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def get_followup_comment(question, answer):
    prompt = f"""You're an interviewer giving a natural, polite, short comment after a candidate answers a question.

Question: {question}
Answer: {answer}

Comment:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 60,
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json()[0]["generated_text"].strip()
    else:
        return "Thanks for sharing that."

def answer_candidate_question(question_text):
    prompt = f"""You are a recruiter. The candidate just asked this question. Respond clearly and conversationally.

Candidate: {question_text}

Reply:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json()[0]["generated_text"].strip()
    else:
        return "That's a thoughtful question. I'd be happy to share more about that later."

def clean_question(q):
    cleaned = re.sub(r"<.*?>", "", q).strip("\u2022- ").strip()
    return cleaned if len(cleaned.split()) > 3 else ""

def wait_for_ready():
    for _ in range(2):
        speak("Are you ready to begin the interview?")
        audio = listen_from_vbcable()
        reply = transcribe(audio)
        if any(yes in reply.lower() for yes in ["yes", "ready", "go ahead", "sure"]):
            return True
        time.sleep(15)
    return False

def run_interview(jd_text, meeting_url):
    skills = extract_skills_and_responsibilities(jd_text)
    dynamic_questions = generate_questions(skills).split("\n")
    filtered_qs = [clean_question(q) for q in dynamic_questions]
    final_qs = [q for q in filtered_qs if q]
    selected_qs = final_qs[:3]
    transcript = ""

    speak("Please take a moment to join the Zoom meeting. We'll begin shortly.")
    time.sleep(45)

    speak("Hi! Welcome to the interview.")

    if not wait_for_ready():
        speak("Looks like you’re not ready right now. Let’s reschedule. Take care!")
        return

    intro_q = "Can you please introduce yourself?"
    speak(intro_q)
    audio = listen_from_vbcable()
    answer = transcribe(audio)
    print(f"Q: {intro_q}\nA: {answer}")
    transcript += f"\nQ: {intro_q}\nA: {answer}"

    for q in selected_qs:
        speak(q)
        audio = listen_from_vbcable()
        answer = transcribe(audio)
        print(f"Q: {q}\nA: {answer}")
        transcript += f"\nQ: {q}\nA: {answer}"
        comment = get_followup_comment(q, answer)
        speak(comment)

    closing_q = "Do you have any questions for us?"
    speak(closing_q)
    audio = listen_from_vbcable()
    candidate_q = transcribe(audio)
    print(f"Candidate asked: {candidate_q}")

    if candidate_q.strip().lower() not in ["no", "nope", "i don't"]:
        reply = answer_candidate_question(candidate_q)
        speak(reply)
        transcript += f"\nCandidate Question: {candidate_q}\nReply: {reply}"

    final_score = score_interview(transcript)
    print("\n📊 Interview Summary:\n" + final_score)
    speak("Thank you for your time. We'll get back to you soon.")

    with open("interview_transcript.txt", "w", encoding="utf-8") as f:
        f.write(f"Zoom Meeting Link: {meeting_url}\n")
        f.write(transcript)
        f.write("\n\nScore:\n" + final_score)

if __name__ == "__main__":
    with open("job_description.txt", "r", encoding="utf-8") as f:
        jd = f.read()

    meeting_url = create_meeting()
    print(f"\n📎 Join the Zoom Meeting: {meeting_url}")
    run_interview(jd, meeting_url)

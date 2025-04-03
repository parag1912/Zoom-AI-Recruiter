# AI Zoom Recruiter 🧑‍💻🙋‍♂️

A voice-interactive AI Interview Bot that conducts real-time interviews over Zoom using Zoom API, Hugging Face LLMs, and ElevenLabs (or local TTS). It listens via VB-Cable, asks intelligent questions based on the job description, comments on answers, scores performance, and answers final queries like a human interviewer.

---

## 📂 Project Structure

```
├── main.py                        # Entry point: creates Zoom, runs interview flow
├── job_parser.py                 # Extracts skills/responsibilities from JD using LLM
├── question_generator.py        # Generates interview questions from extracted skills
├── scoring.py                   # Scores interview transcript via LLM
├── zoom_integration.py          # Creates Zoom meeting using Zoom API
├── voice_interface.py           # Text-to-speech (speak), audio listening, transcription
├── test_api.py                  # Test endpoints for LLMs, ElevenLabs, Zoom
├── job_description.txt          # Sample job description for interview
├── requirements.txt             # Python dependencies
├── config.py                    # Stores Hugging Face & ElevenLabs API keys
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone <your-repo-url>
cd AI-Zoom-Interview-Bot
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure APIs
Edit `config.py` with your keys:
```python
HUGGINGFACE_API_KEY = "your-hf-key"
ELEVENLABS_API_KEY = "your-elevenlabs-key"
ZOOM_JWT = "your-zoom-jwt"
```

### 5. Setup VB-Cable
- Download from https://vb-audio.com/Cable
- Set **VB-Cable Output** as Zoom Speaker
- Set **VB-Cable Input** as Zoom Mic

### 6. Run the Interview
```bash
python main.py
```

---

## 🌐 Architecture Overview

**Input:** Job description → Skill extraction → Question generation  
**Interview Flow:**
1. Create Zoom link
2. Ask "Are you ready?" and wait for confirmation
3. Ask intro + 3 dynamic questions
4. After each answer, give a human-like follow-up
5. Ask if candidate has any questions, answer them
6. Score interview
7. Save full transcript + summary

**Output:** `interview_transcript.txt` with responses and LLM feedback

---

## ⚖️ Key Decisions Made

| Component | Decision | Why It Matters |
|----------|---------|----------------|
| Hugging Face | Used `falcon-7b-instruct` | Free and supports custom prompts |
| ElevenLabs | For TTS voice | More natural than pyttsx3/gTTS |
| VB-Cable | Audio routing | Seamless audio loop from Zoom speaker to bot listener |
| Prompt Engineering | Few-shot prompts for feedback, comment, and scoring | Ensures human-like response instead of robotic tone |
| Retry logic | For candidate readiness check | Mimics real human interaction flow |

---

## 🔧 Features
- ✅ Creates Zoom link via API
- 🎙️ Listens to candidate via VB-Cable
- 🎤 Speaks questions and comments with TTS
- ❓ Asks follow-ups and final question
- ✏️ Scores performance using Hugging Face
- 📄 Outputs transcript and score

---

## 📅 Coming Soon (Ideas)
- Streamlit Web Interface
- Multiple voice styles
- Real-time dashboard with scoring breakdown
- Candidate emotion detection via webcam
- Persistent database logging (MongoDB/SQLite)

---

Made with ❤️ by [Your Name / Team].


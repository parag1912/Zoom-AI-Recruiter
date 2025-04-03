# zoom_integration.py
import requests
from base64 import b64encode
from config import ZOOM_API_KEY, ZOOM_API_SECRET, ZOOM_ACCOUNT_ID

# ✅ Replace with your actual Zoom email
USER_EMAIL = ""

def get_access_token():
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ZOOM_ACCOUNT_ID}"
    auth_str = f"{ZOOM_API_KEY}:{ZOOM_API_SECRET}"
    b64_auth = b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, headers=headers)
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        print("❌ Failed to get access token")
        print("Status:", res.status_code)
        print("Response:", res.text)
        return None

def create_meeting():
    token = get_access_token()
    if not token:
        return None

    url = f"https://api.zoom.us/v2/users/{USER_EMAIL}/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    meeting_data = {
        "topic": "AI Interview",
        "type": 1,  # Instant meeting
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True
        }
    }

    res = requests.post(url, headers=headers, json=meeting_data)
    if res.status_code in [200, 201]:
        meeting_url = res.json().get("join_url")
        print("✅ Zoom meeting created successfully!")
        print("Meeting URL:", meeting_url)
        return meeting_url
    else:
        print("❌ Failed to create meeting")
        print("Status:", res.status_code)
        print("Response:", res.text)
        return None

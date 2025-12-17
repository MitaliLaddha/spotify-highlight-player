import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("ERROR: ACCESS_TOKEN missing")
    exit(1)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# CONFIG (will make this user input later) 
START_SECONDS = 45      # where highlight starts
HIGHLIGHT_DURATION = 30  # how long to play (seconds)

# 1. Seek to start
seek_ms = START_SECONDS * 1000
seek_url = f"https://api.spotify.com/v1/me/player/seek?position_ms={seek_ms}"

seek_response = requests.put(seek_url, headers=headers)

if seek_response.status_code not in (200, 204):
    print("Seek failed:", seek_response.status_code)
    exit(1)

print(f"Seeked to {START_SECONDS}s")

# 2. Wait for highlight duration
print(f"Playing highlight for {HIGHLIGHT_DURATION} seconds...")
time.sleep(HIGHLIGHT_DURATION)

# 3. Skip to next track
next_url = "https://api.spotify.com/v1/me/player/next"
next_response = requests.post(next_url, headers=headers)

if next_response.status_code not in (200, 204):
    print("Skip failed:", next_response.status_code)
else:
    print("Skipped to next song 🎶")

import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("ERROR: ACCESS_TOKEN not found in .env")
    exit(1)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = "https://api.spotify.com/v1/me/player"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    if data is None:
        print("No active playback")
    else:
        track = data["item"]
        artists = ", ".join(a["name"] for a in track["artists"])

        print("Now Playing:")
        print("Song:", track["name"])
        print("Artist:", artists)
        print("Progress (ms):", data["progress_ms"])
        print("Duration (ms):", track["duration_ms"])
else:
    print(response.json())

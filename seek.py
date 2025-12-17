import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("ERROR: ACCESS_TOKEN not found")
    exit(1)

# Seek time in seconds
seek_seconds = 45
seek_ms = seek_seconds * 1000

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = f"https://api.spotify.com/v1/me/player/seek?position_ms={seek_ms}"

response = requests.put(url, headers=headers)

print("Status:", response.status_code)

if response.status_code in (200, 204):
    print(f"Successfully seeked to {seek_seconds} seconds")
else:
    print("Error:", response.status_code)
    if response.text:
        print(response.text)


import requests

BASE_URL = "https://api.spotify.com/v1"

class SpotifyClient:
    def __init__(self, access_token):
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    def get_current_playback(self):
        url = f"{BASE_URL}/me/player"
        return requests.get(url, headers=self.headers)

    def seek(self, position_ms):
        url = f"{BASE_URL}/me/player/seek?position_ms={position_ms}"
        return requests.put(url, headers=self.headers)

    def next_track(self):
        url = f"{BASE_URL}/me/player/next"
        return requests.post(url, headers=self.headers)

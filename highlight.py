import time
from spotify_auth import get_access_token
from spotify_client import SpotifyClient
from utils import parse_time_to_seconds

def main():
    start_input = input("Enter highlight start time (seconds or mm:ss): ")
    duration_input = input("Enter highlight duration (seconds): ")

    start_seconds = parse_time_to_seconds(start_input)
    duration_seconds = int(duration_input)

    access_token = get_access_token()
    spotify = SpotifyClient(access_token)

    print(f"Seeking to {start_seconds}s...")
    spotify.seek(start_seconds * 1000)

    print(f"Playing highlight for {duration_seconds}s...")
    time.sleep(duration_seconds)

    spotify.next_track()
    print("Skipped to next song.")

if __name__ == "__main__":
    main()

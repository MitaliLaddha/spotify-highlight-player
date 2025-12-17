import time
from spotify_auth import get_access_token
from spotify_client import SpotifyClient
from utils import parse_time_to_seconds
from storage import load_highlights, save_highlights

def main():
    access_token = get_access_token()
    spotify = SpotifyClient(access_token)

    playback_response = spotify.get_current_playback()

    if playback_response.status_code == 204:
        print("Playback inactive. Resuming...")
        spotify.play()
        time.sleep(1)
        playback_response = spotify.get_current_playback()

    if playback_response.status_code != 200:
        print("No active playback even after resume.")
        return


    data = playback_response.json()
    track = data["item"]

    if not track:
        print("No track playing.")
        return

    track_id = track["id"]
    track_name = track["name"]
    artists = ", ".join(a["name"] for a in track["artists"])

    print(f"Now playing: {track_name} — {artists}")

    highlights = load_highlights()

    if track_id in highlights:
        start_seconds = highlights[track_id]["start"]
        duration_seconds = highlights[track_id]["duration"]
        print("Using saved highlight")
    else:
        print("No highlight saved for this song.")
        start_input = input("Enter highlight start time (seconds or mm:ss): ")
        duration_input = input("Enter highlight duration (seconds): ")

        start_seconds = parse_time_to_seconds(start_input)
        duration_seconds = int(duration_input)

        highlights[track_id] = {
            "start": start_seconds,
            "duration": duration_seconds
        }
        save_highlights(highlights)
        print("Highlight saved ")

    # Apply highlight
    seek_resp = spotify.seek(start_seconds * 1000)
    print("Seek status:", seek_resp.status_code)
    time.sleep(0.5)

    print(f"Playing highlight for {duration_seconds} seconds...")
    time.sleep(duration_seconds)
    next_resp = spotify.next_track()
    print("Next status:", next_resp.status_code)

    print("Skipped to next song..")

if __name__ == "__main__":
    main()

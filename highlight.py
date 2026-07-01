import time
from spotify_auth import get_access_token
from spotify_client import SpotifyClient
from utils import parse_time_to_seconds
from storage import get_highlight, save_highlight, delete_highlight

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
    track = data.get("item")

    if not track:
        print("No track playing.")
        return

    track_id = track["id"]
    track_name = track["name"]
    artists = ", ".join(a["name"] for a in track["artists"])

    print(f"Now playing: {track_name} — {artists}")

    # Ask SQLite database for this specific track's highlight
    saved = get_highlight(track_id)

    if saved:
        print("Saved highlight found in database")
        print(f"Start: {saved['start']}s, Duration: {saved['duration']}s")

        print("\nChoose an option:")
        print("1. Play saved highlight")
        print("2. Edit highlight")
        print("3. Delete highlight")
        print("4. Skip song")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            start_seconds = saved["start"]
            duration_seconds = saved["duration"]

        elif choice == "2":
            start_input = input("Enter new start time (seconds or mm:ss): ")
            duration_input = input("Enter new duration (seconds): ")

            start_seconds = parse_time_to_seconds(start_input)
            duration_seconds = int(duration_input)
            
            save_highlight(track_id, start_seconds, duration_seconds)
            print("Highlight updated in database.")

        elif choice == "3":
            delete_highlight(track_id)
            print("Highlight deleted from database.")
            spotify.next_track()
            return

        elif choice == "4":
            spotify.next_track()
            return

        else:
            print("Invalid choice.")
            return

    else:
        print("No highlight saved for this song.")
        start_input = input("Enter highlight start time (seconds or mm:ss): ")
        duration_input = input("Enter highlight duration (seconds): ")

        start_seconds = parse_time_to_seconds(start_input)
        duration_seconds = int(duration_input)

        save_highlight(track_id, start_seconds, duration_seconds)
        print("Highlight saved to database.")

    # Apply highlight
    seek_resp = spotify.seek(start_seconds * 1000)
    print("Seek status:", seek_resp.status_code)
    time.sleep(0.5)

    print(f"Playing highlight for {duration_seconds} seconds...")
    time.sleep(duration_seconds)
    next_resp = spotify.next_track()
    print("Next status:", next_resp.status_code)
    print("Skipped to next song.")

if __name__ == "__main__":
    main()
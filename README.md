# Spotify Highlight Player 🎧

A Python-based tool that plays only the most important highlight segments of Spotify songs instead of full tracks.

> Note: Spotify must be actively playing a song for playback control APIs to work.

## Motivation
Often, we don’t want to listen to an entire song — just the best 30–90 seconds.  
Spotify doesn’t offer this natively.

This project adds a **highlight playback mode** by programmatically controlling Spotify using the Spotify Web API.

## Features
- OAuth 2.0 authentication with automatic token refresh
- Read current playback state
- Seek to any timestamp in a song
- Play a fixed highlight duration and auto-skip
- Per-song highlight memory (saved locally)
- Robust handling of paused or inactive playback
- Clean, modular architecture

## How it works (High level)
1. Authenticates with Spotify using OAuth
2. Reads the currently playing track
3. Checks if a highlight is already saved for the song
4. If yes → plays it automatically  
   If no → asks the user once and saves it
5. Seeks → waits → skips to next track

## Project Structure
```text
spotify-highlight-player/
├── spotify_auth.py      # OAuth + token refresh
├── spotify_client.py    # Spotify Web API calls
├── highlight.py         # Main highlight playback logic
├── storage.py           # Persistent highlight storage
├── utils.py             # Helper functions (time parsing)
├── highlights.json      # (ignored) user highlight data
├── .env.example
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+
- A Spotify account
- Spotify desktop app running

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/spotify-highlight-player.git
cd spotify-highlight-player
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
```

### 3. Spotify Developer Configuration

1. Go to [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add the following Redirect URI:

```
http://127.0.0.1:8888/callback
```

4. Copy the **Client ID** and **Client Secret**

### 4. Environment variables

Create a `.env` file using `.env.example` and fill in your credentials:

```env
CLIENT_ID=
CLIENT_SECRET=
REFRESH_TOKEN=
REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 5. Run the app

Make sure Spotify is open and a song is playing:

```bash
python highlight.py
```

## Notes

* This project controls Spotify playback; it does not stream or download audio.
* Highlights are stored locally per track ID.
* Designed primarily as a learning project for APIs, OAuth, and systems programming.



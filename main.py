import json
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from utils import settings

CACHE_FILE = ".cache"

# Load credentials from the TOML file
CLIENT_ID = settings.config["General"]["SpotifyClientID"]
CLIENT_SECRET = settings.config["General"]["SpotifyClientSecret"]
REDIRECT_URI = settings.config["General"]["SpotifyRedirectURI"]

# Define the scope for accessing liked songs
SCOPE = "user-library-read"

def load_cache():
    """Load the cache file."""
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(data):
    """Save data to the cache file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def get_spotify_client():
    """Authenticate with Spotify using cached tokens."""
    cache = load_cache()

    # Check if the access token is expired
    if "expires_at" not in cache or cache["expires_at"] <= time.time():
        print("Access token expired. Refreshing...")
        auth_manager = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE_FILE  # Use the .cache file
        )
        token_info = auth_manager.refresh_access_token(cache["refresh_token"])

        # Update cache with new token information
        cache.update(token_info)
        save_cache(cache)

    # Use the valid access token
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_FILE  # Use the .cache file
    )
    return spotipy.Spotify(auth_manager=auth_manager)

def parse_liked_songs():
    sp = get_spotify_client()
    results = sp.current_user_saved_tracks(limit=100)

    while results:
        for item in results['items']:
            track = item['track']
            artist_name = track['artists'][0]['name']
            song_name = track['name']
            print(f"Song: {song_name}, Artist: {artist_name}")

            artist_id = track['artists'][0]['id']
            artist = sp.artist(artist_id)
            genres = artist.get('genres', [])
            if genres:
                print(f"Genres: {', '.join(genres)}")
            else:
                print("No genres found for this artist.")
            print("-" * 40)

        if results['next']:
            results = sp.next(results)
        else:
            break

if __name__ == "__main__":
    parse_liked_songs()

import json
import time
from collections import Counter

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from utils import settings

CACHE_FILE = ".cache"

# Load credentials from the TOML file
CLIENT_ID = settings.config["General"]["SpotifyClientID"]
CLIENT_SECRET = settings.config["General"]["SpotifyClientSecret"]
REDIRECT_URI = settings.config["General"]["SpotifyRedirectURI"]

# Define the scope for accessing liked songs
SCOPE = "user-library-read user-read-private user-read-playback-state playlist-read-private"

# Define whether to include public playlists
INCLUDE_PUBLIC_PLAYLISTS = False  # Set this to True to include public playlists

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

def fetch_all_playlists():
    """Fetch all playlists for the authenticated user."""
    sp = get_spotify_client()
    playlists = []
    results = sp.current_user_playlists(limit=50)  # Adjust limit if needed
    playlists.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
        
    return playlists

def fetch_genres_from_track(track):
    """Fetch genres of the artist of the given track."""
    sp = get_spotify_client()
    
    # Check if the track is a local file (Spotify returns None for local tracks)
    if track is None or not track.get('artists') or track['id'] is None:
        print(f"Skipping local track: {track.get('name', 'Unknown')}")
        return []

    artist_id = track['artists'][0]['id']
    try:
        artist_info = sp.artist(artist_id)
        return artist_info.get('genres', [])
    except Exception as e:
        print(f"Error fetching genres for {track['name']} by {track['artists'][0]['name']}: {e}")
        return []

def parse_playlists_for_genres():
    """Parse all playlists for genres and count their frequency."""
    sp = get_spotify_client()
    genres_counter = Counter()
    playlists = fetch_all_playlists()
    
    # Get the current user's ID for comparison
    current_user_id = sp.current_user()['id']

    for playlist in playlists:
        # Only process playlists that are either owned by the user or public (if INCLUDE_PUBLIC_PLAYLISTS is True)
        is_owned_by_user = playlist['owner']['id'] == current_user_id
        is_public = playlist['public']
        
        if is_owned_by_user or (INCLUDE_PUBLIC_PLAYLISTS and is_public):
            print(f"Processing playlist: {playlist['name']}")
            tracks = []
            results = sp.playlist_tracks(playlist['id'], limit=50)
            tracks.extend(results['items'])
            
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            
            for item in tracks:
                track = item['track']
                if track:  # Check if track is not None
                    print(f"Processing song: {track['name']} - Artist ID: {track['artists'][0]['id']}")  # Debug: Print song title
                    genres = fetch_genres_from_track(track)
                    for genre in genres:
                        genres_counter[genre] += 1

    return genres_counter

def display_genre_frequencies():
    """Display the frequency of each genre."""
    genres_counter = parse_playlists_for_genres()
    
    print("\nGenre Frequencies:")
    for genre, count in genres_counter.most_common():
        print(f"{genre}: {count}")

if __name__ == "__main__":
    display_genre_frequencies()

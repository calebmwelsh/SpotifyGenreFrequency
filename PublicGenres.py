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
PUBLIC_PLAYLIST_URI = settings.config["General"]["SpotifyPublicPlaylistURI"]

# Define the scope for accessing liked songs
SCOPE = "user-library-read user-read-private user-read-playback-state playlist-read-private"

# Define whether to include public playlists
INCLUDE_PUBLIC_PLAYLISTS = True  # Set this to True to include public playlists

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

def fetch_playlists_from_user(user_id):
    """Fetch playlists of a specific user."""
    sp = get_spotify_client()

    playlists = []
    results = sp.user_playlists(user_id, limit=50)  # Get playlists of the user
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

def display_user_playlist_genres(user_id):
    """Display genre frequencies for a specific user's playlists."""
    sp = get_spotify_client()
    genres_counter = Counter()
    
    # Fetch playlists from another user
    playlists = fetch_playlists_from_user(user_id)

    for playlist in playlists:
        # Skip if the playlist is private and we're not including public ones
        if not playlist['public'] and not INCLUDE_PUBLIC_PLAYLISTS:
            continue
        
        print(f"Processing playlist: {playlist['name']}")
        tracks = []
        results = sp.playlist_tracks(playlist['id'], limit=50)
        tracks.extend(results['items'])

        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        for item in tracks:
            track = item['track']
            if track:
                print(f"Processing song: {track['name']} - Artist ID: {track['artists'][0]['id']}")  # Debug: Print song title
                genres = fetch_genres_from_track(track)
                for genre in genres:
                    genres_counter[genre] += 1

    # Display genre frequencies
    print("\nGenre Frequencies:")
    for genre, count in genres_counter.most_common():
        print(f"{genre}: {count}")
        
def get_user_id_from_playlist_uri(playlist_uri):
    """Extract user ID from the playlist URI."""
    # Extract playlist ID from the URI
    playlist_id = playlist_uri.split("/")[-1].split("?")[0]
    
    # Get Spotify client
    sp = get_spotify_client()
    
    # Fetch the playlist details using the playlist ID
    playlist_details = sp.playlist(playlist_id)
    
    # Extract and return the user ID (the owner of the playlist)
    user_id = playlist_details['owner']['id']
    return user_id

# Get spotify user id based on playlist uri
user_id = get_user_id_from_playlist_uri(PUBLIC_PLAYLIST_URI)
print(f"The user ID for the playlist is: {user_id}")

display_user_playlist_genres(user_id)

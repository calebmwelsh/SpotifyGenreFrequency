import spotipy
from spotipy.oauth2 import SpotifyOAuth

from utils import settings

# Load credentials from the TOML file
CLIENT_ID = settings.config["General"]["SpotifyClientID"]
CLIENT_SECRET = settings.config["General"]["SpotifyClientSecret"]
REDIRECT_URI = settings.config["General"]["SpotifyRedirectURI"]

SCOPE = "playlist-read-private"

def get_spotify_client():
    """Authenticate with Spotify using cached tokens."""
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    return spotipy.Spotify(auth_manager=auth_manager)

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

# Example usage with a playlist URI
playlist_uri = "https://open.spotify.com/playlist/1NMBntrpcYybqbthT3eapO?nd=1&dlsi=a8d1d2fe9b8447a4"  # Replace with the actual URI
user_id = get_user_id_from_playlist_uri(playlist_uri)
print(f"The user ID for the playlist is: {user_id}")

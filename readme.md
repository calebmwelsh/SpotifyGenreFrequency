# Spotify Genre Frequency Analyzer

This Python project analyzes genre frequencies in Spotify playlists.

## Features

- Fetches tracks from a public Spotify playlist
- Extracts genres for each track
- Calculates and displays genre frequencies

## Prerequisites

- Python 3.6+
- Spotify Developer account
- `spotipy` library

## Spotify Developer Project Setup Guide

This section will walk you through the steps to set up a Spotify Developer Dashboard and integrate it with this repo.

## Prerequisites

- A Spotify Developer account. If you don't have one, sign up at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
- Basic knowledge of programming and API integrations.

## Steps to Set Up the Project

### 1. Create a New Application on Spotify Developer Dashboard

1. Navigate to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Log in with your Spotify account or create a new account if you don't have one.
3. Click on **Create an App**.
4. Fill in the necessary details for your app, including:
   - **App Name**: The name of your application.
   - **App Description**: A short description of what your app does.
   - **Redirect URI**: The URI to which the user will be redirected after authentication. This is important for OAuth integration. (http://localhost:8888/callback should work fine)
   - **App Privacy Policy URL**: Optional, but recommended for production applications.

5. Agree to the Spotify Developer Terms and click **Create**.

### 2. Get Your Client ID and Client Secret

Once your app is created, you'll be redirected to your application's dashboard. Here, you can find:
- **Client ID**: This is a unique identifier for your application.
- **Client Secret**: This is a secret key used for authentication and should be kept secure.

Keep these credentials safe, as they will be used to authenticate your application.

### 3. Set Up Authentication (OAuth)

Spotify APIs use OAuth 2.0 for authentication. To get started:

1. Set up your redirect URI in the Spotify Developer Dashboard (ensure it matches the URI you specified during app creation).
2. Use your **Client ID** and **Client Secret** to authenticate users through OAuth.
   

## Repo Installation

1. Clone the repository:
```bash
git clone https://github.com/calebmwelsh/SpotifyGenreFrequency
cd SpotifyGenreFrequency
```
2. Install dependencies:
pip install -r requirements.txt

3. Set up Spotify credentials in `config.toml.temp`:  
```
[General]
SpotifyClientID = "your_client_id"
SpotifyClientSecret = "your_client_secret"
SpotifyRedirectURI = "your_redirect_uri"
SpotifyPublicPlaylistURI = "a_public_playlist_uri"
```

4. Remove `.temp` from `config.toml.temp`

## Usage

This project includes two main scripts for analyzing the frequency of music genres based on a user's playlist:

### 1. `PublicGenres.py` - Using Public Playlists

The `PublicGenres.py` script allows you to analyze the genre frequency of a **public playlist**. It can identify the frequency of genres based on the tracks from any user using the Spotify Web API. However two conditions must be met.

- Their playlists must be public
- Need the URI of one of the public playlists

### 2. `PrivateGenres.py` - Using private Playlists

The `PrivateGenres.py` script allows you to analyze the genre frequency of a **private playlist**. It can identify the genres of tracks from your private playlists by using the Spotify Web API.

#### How to Use:
1. Ensure that you have your Spotify **Client ID**, **Client Secret**, and **RedirectURI** set up properly.
2. In `PublicGenres.py`, provide the **public playlist URI** you want to analyze in the TOML config.
3. Run the script to retrieve the genre frequency for the tracks in the public or private playlist.

```bash
python PublicGenres.py 
```
or
```bash
python PrivateGenres.py 
```
4. OAuth2 will trigger through your browser, authenticate by allowing the project.

## Example Output

Processing playlist: My Favorite Playlist  
Processing song: Song Name - Artist Name  
...  
Genre Frequencies:  
Pop: 25  
Rock: 15  
Hip-Hop: 10  
Jazz: 5  
...  

## Project Structure

SpotifyGenreFrequency  
├── PrivateGenres.py  
├── PublicGenres.py  
├── requirements.txt  
└── utils/  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── settings.toml   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; └── .config.template.toml  

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/)
- [Spotify Developer](https://developer.spotify.com/)

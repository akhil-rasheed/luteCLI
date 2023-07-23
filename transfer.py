import colorama
from colorama import Fore, Style
from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyPKCE
import webbrowser, subprocess, os
import logging
import argparse
import asyncio

colorama.init()

parser = argparse.ArgumentParser(description='Lute - Transfer local music to Spotify')
parser.add_argument('--folder-path', default='./jm', help='Path to the folder containing music files')

args = parser.parse_args()

PROCESS_FOLDER_PATH = args.folder_path

CLIENT_ID = 'a8f4a5a9ad14447c84fe7badb8b573bb'
REDIRECT_URI = 'http://localhost:8000/callback'
SCOPE = 'playlist-read-private playlist-modify-public'
FOLDER_PATH = './playlists'

logging.basicConfig(level=logging.INFO, filename='log.txt')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = False

sp_oauth = SpotifyPKCE(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

def read_file(file_path):
    """Read a text file and return its contents as a list of lines."""
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except IOError as e:
        logger.error(f"Error reading file: {file_path} - {str(e)}")
    return []

def create_playlist(sp, playlist_name):
    """Create a playlist with the given name."""
    try:
        playlist = sp.user_playlist_create(sp.current_user()['id'], playlist_name)
        logger.info(f"Playlist '{playlist_name}' created")
        return playlist
    except spotipy.SpotifyException as e:
        logger.error(f"Error creating playlist: {str(e)}")
    return None

def search_track(sp, track_name):
    """Search for a track and return its URI if found."""
    try:
        results = sp.search(q=track_name, type='track', limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['uri']
        else:
            logger.warning(f"Track not found: {track_name}")
    except spotipy.SpotifyException as e:
        logger.error(f"Error searching track: {str(e)}")
    return None

def add_track_to_playlist(sp, playlist_id, track_uri):
    """Add a track to the playlist with the given ID."""
    try:
        sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, [track_uri])
    except spotipy.SpotifyException as e:
        logger.error(f"Error adding track to playlist: {str(e)}")

def create_playlists(sp):
    """Create playlists from text files in the specified folder."""
    for file_name in os.listdir(FOLDER_PATH):
        if file_name.endswith('.txt'):
            file_path = os.path.join(FOLDER_PATH, file_name)
            playlist_name = 'LuteCLI: ' + os.path.splitext(file_name)[0] 

            lines = read_file(file_path)
            if lines:
                playlist =  create_playlist(sp, playlist_name)
                if playlist:
                    for line in lines:
                        track_name = line.strip()
                        track_uri =  search_track(sp, track_name)
                        if track_uri:
                             add_track_to_playlist(sp, playlist['id'], track_uri)

def run_process():
    subprocess.run(["python", "process.py", PROCESS_FOLDER_PATH])

@app.route('/callback')
def handle_callback():
    code = request.args.get('code')
    access_token = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=access_token)
    create_playlists(sp)
    print(Fore.GREEN + 'Authorization successful, you may now close this window' + Style.RESET_ALL)
    return 'Authorization successful, you may now close this window'

if __name__ == '__main__':
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    sp_oauth = SpotifyPKCE(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

    auth_url = sp_oauth.get_authorize_url()
    webbrowser.open_new(auth_url)

    app.run(host='localhost', port=8000)

# Lute - Transfer Local Music to Spotify

Lute is a Python script that allows you to transfer your local music files to Spotify by creating playlists based on the contents of those files. The script extracts song titles and artists from MP3 files in a specified folder and creates playlists on your Spotify account.
Prerequisites

Before running the script, make sure you have the following:

1. Python 3 installed on your system.
2. A Spotify Developer Account: Spotify Developer Dashboard.
3. Create a new Spotify app to get the Client ID for the script.

Setup

Clone or download this repository to your local machine.
Install the required dependencies using pip:

    pip install -r requirements.txt

Set up Spotify API credentials:
    Create a new app on the Spotify Developer Dashboard and obtain the "Client ID."
    Add "http://localhost:8000/callback" as a Redirect URI for your app on the Spotify Developer Dashboard.
    Place your MP3 files in a folder (e.g., "jm" folder) within the project directory.

Usage
    Open a terminal or command prompt and navigate to the project directory.
    To process the local music files and create the playlists, run the following command:

    python transfer.py --folder-path <path_to_your_mp3_folder>

Replace <path_to_your_mp3_folder> with the path to the folder containing your MP3 files.


Follow the authentication instructions that appear in your web browser. The script will prompt you to log in to your Spotify account and grant access to create playlists.

Once the script completes the authentication process and creates playlists, you can close the browser window and return to the terminal.

Notes

The script uses the "eyed3" library to read MP3 metadata and extract song titles and artist names. Make sure your music files have proper ID3 tags for accurate results.

Playlists are created under the name "LuteCLI: <folder_name>" on your Spotify account.

If any errors occur during the transfer process, check the "log.txt" file for more information.

The script will automatically open your default web browser for Spotify authentication. (Currently works only on linux)

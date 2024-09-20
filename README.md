# Spotify Playlist Randomizer

If you are as me you are probably tired of how bad/biased is the shuffling on Spotify. This Python application allows you to randomize your Spotify playlists in place.

## Features

- Randomize tracks in any Spotify playlist you own or have edit access to
- Secure authentication using Spotify's Authorization Code Flow with PKCE
- Backup and restore functionality to prevent data loss
- Fisher-Yates shuffle algorithm as a randomizer.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- A Spotify account
- A Spotify Developer account and a registered Spotify application

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/Wilowisp98/spotify_randomizer
   cd spotify_randomizer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Spotify Developer application:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Set the Redirect URI to `http://localhost:8080` in your app settings

4. Run the application:
   ```
   python __main__.py
   ```
   or
   ```
   python application
   ```

   On first run, you'll be prompted to enter your Spotify Client ID. This will be saved in `client_id.txt` for future use.

## Usage

1. Run the application:

2. If it's your first time running the app, you'll be asked to enter your Spotify Client ID.

3. A browser window will open for you to log in to Spotify and authorize the application.

4. Once authorized, you'll be prompted to enter the Spotify playlist link you want to randomize.

5. Confirm that you want to randomize the playlist.

6. The application will shuffle the tracks and update the playlist on Spotify.

## Backup and Restore

If an error occurs during randomization, the application will attempt to restore the original playlist order. If this fails, a backup file will be created with the format `backup_PLAYLIST_ID.txt`.

To restore from a backup:

1. Run the application.
2. When prompted, choose the backup file you want to restore from.
3. Confirm the restoration.
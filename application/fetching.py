import json
import requests
import random
import os

class SpotifyAPI:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.auth.access_token}",
            "Content-Type": "application/json"
        }

    def fisher_yates_shuffle(self, items):
        for i in range(len(items) - 1, 0, -1):
            j = random.randint(0, i)
            items[i], items[j] = items[j], items[i]
        return items

    def fetch_playlist(self, playlist_id):
        playlist_url = f'{self.base_url}/playlists/{playlist_id}/tracks'
        playlist_content = []
        
        response = requests.get(url=playlist_url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        for track in data['tracks']['items']:
            playlist_content.append(track['track']['uri'])

        return playlist_content
    
    def add_tracks_to_playlist(self, playlist_id, track_uris):
        playlist_url = f'{self.base_url}/playlists/{playlist_id}/tracks'
        
        for i in range(0, len(track_uris), 100):
            chunk = track_uris[i:i+100]
            data = {'uris': chunk}
            response = requests.post(url=playlist_url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()

    def clear_playlist(self, playlist_id, current_tracks):
        playlist_id = playlist_id.split('?')[0] 
        endpoint = f'{self.base_url}/playlists/{playlist_id}/tracks'
        
        if not current_tracks:
            print(f"Playlist {playlist_id} is already empty.")
            return True
        
        for i in range(0, len(current_tracks), 100):
            chunk = current_tracks[i:i+100]
            data = json.dumps({'tracks': [{'uri': track} for track in chunk]})
            response = requests.delete(url=endpoint, headers=self.headers, data=data)
            
            if response.status_code != 200:
                print(f"Failed to clear playlist. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        print(f"Removed {len(current_tracks)} tracks from playlist {playlist_id}")
        return True

    def add_tracks_to_playlist(self, playlist_id, track_uris):

        playlist_id = playlist_id.split('?')[0] 
        playlist_url = f'{self.base_url}/playlists/{playlist_id}/tracks'
        
        for i in range(0, len(track_uris), 100):
            chunk = track_uris[i:i+100]
            data = json.dumps({'uris': chunk})
            response = requests.post(url=playlist_url, headers=self.headers, data=data)
            
            if response.status_code != 201:
                print(f"Failed to add tracks. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        print(f"Added {len(track_uris)} tracks to playlist {playlist_id}")
        return True

    def randomize_playlist_in_place(self, playlist_id):

        try:
            original_tracks = self.fetch_playlist(playlist_id)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching playlist: {e}")
            return

        if not original_tracks:
            print(f"Playlist {playlist_id} is empty or not accessible.")
            return

        backup_tracks = original_tracks.copy()

        shuffled_tracks = self.fisher_yates_shuffle(original_tracks)
        
        if not self.clear_playlist(playlist_id, shuffled_tracks):   
            print("Failed to clear the playlist. Creating backup with original tracks...")
            self.add_tracks_to_playlist(playlist_id, backup_tracks)
            return

        if not self.add_tracks_to_playlist(playlist_id, shuffled_tracks):

            print("Failed to add shuffled tracks. Restoring original tracks...")

            if not self.add_tracks_to_playlist(playlist_id, backup_tracks):

                print("Failed to add backup tracks. Creating backup file...")
                backup_file = open(f"backup_{playlist_id.split('?')[0]}.txt", "w")
                backup_file.write(playlist_id + '\n')

                for track in backup_tracks:

                    backup_file.write(track + '\n')
                    
                print("Backup file created with success.")
                return 
            
            print("Original tracks restored with success.")
            return

        print(f"Playlist has been successfully randomized in place!")
import os
from authentication import SpotifyAuth
from fetching import SpotifyAPI

def get_client_id():
    if not os.path.isfile('client_id.txt'):
        print("To use this Spotify Playlist Randomizer, you need your own Spotify Client ID.")
        print("If you don't have one, follow these steps:")
        print("1. Go to https://developer.spotify.com/dashboard/")
        print("2. Log in with your Spotify account")
        print("3. Click 'Create an App'")
        print("4. Give your app a name and description")
        print("5. Once created, you'll see your Client ID")
        print("6. In your app settings, add http://localhost:8080 as a Redirect URI")

        client_id = input("Enter your Spotify Client ID: ").strip()
        with open("client_id.txt", "w") as file:
            file.write(client_id)
    else:
        with open("client_id.txt", "r") as file:
            client_id = file.read().strip()

    return client_id

def to_bool(word):
    return word.lower() in ['yes', 'y', '1', 'true']

def get_backup_file():
    current_dir = os.getcwd()
    backup_files = [file for file in os.listdir(current_dir) if file.startswith('backup')]

    if not backup_files:
        return None

    print("Available backup files:")
    for i, file in enumerate(backup_files, 1):
        print(f"{i}. {file}")

    while True:
        choice = input("Enter the number of the backup file you want to use (or 'n' for none): ").strip().lower()
        if choice == 'n':
            return None
        try:
            index = int(choice) - 1
            if 0 <= index < len(backup_files):
                return backup_files[index]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'n'.")

def process_backup(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    playlist_id = lines[0]
    uris = lines[1:]
    return playlist_id, uris

def delete_backup(file_path):
    try:
        os.remove(file_path)
        print(f"Backup file {file_path} has been deleted.")
    except Exception as e:
        print(f"Error deleting backup file: {e}")

def get_playlist_link():
    while True:
        playlist_link = input("Enter the Spotify playlist link that you want to randomize: ").strip()
        if playlist_link.startswith("https://open.spotify.com/playlist/"):
            return playlist_link.split('/')[-1].split('?')[0]
        else:
            print("Invalid playlist link. Please provide a valid Spotify playlist URL.")

if __name__ == "__main__":
    client_id = get_client_id()
    scope = 'playlist-modify-public playlist-modify-private playlist-read-private'
    
    auth = SpotifyAuth(client_id, scope)
    try:
        auth.authorize()
        api = SpotifyAPI(auth)
        
        backup_file = get_backup_file()
        if backup_file:
            playlist_id, uris = process_backup(backup_file)
            confirm = input(f"Are you sure you want to restore the playlist from {backup_file}? (yes/no): ")
            if to_bool(confirm):
                api.add_tracks_to_playlist(playlist_id, uris)
                print("Playlist restored successfully from backup!")
                delete_backup(backup_file)
            else:
                print("Backup restoration cancelled.")
        else:
            playlist_id = get_playlist_link()
            confirm = input(f"Are you sure you want to randomize the playlist with ID {playlist_id}? (yes/no): ")
            if to_bool(confirm):
                api.randomize_playlist_in_place(playlist_id)
                print("Playlist successfully randomized!")
            else:
                print("Randomization cancelled.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check the instructions and try again.")
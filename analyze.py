import os
import src.analyzer as analyzer
from src.filereader import FileReader
from termcolor import colored
from src.db import SQLiteDatabase

MUSICS_FOLDER_PATH = "mp3"

if __name__ == '__main__':
    db = SQLiteDatabase()

    for filename in os.listdir(MUSICS_FOLDER_PATH):
        if filename.endswith(".wav"):
            # Create a FileReader instance for the current WAV file
            file_path = os.path.join(MUSICS_FOLDER_PATH, filename)
            reader = FileReader(file_path)
            # Parse audio data from the WAV file
            audio = reader.parse_audio()

            # Check if a song with the same file hash exists in the database
            song = db.get_song_by_filehash(audio['file_hash'])

            # Add the song to the database if it doesn't exist
            if not song:
                song_id = db.add_song(filename, audio['file_hash'])
            else:
                song_id = song['id']

            print(colored(f"Analyzing music: {filename}", "green"))

            # Check if the song already has fingerprints in the database
            hash_count = db.get_song_hashes_count(song_id)
            if hash_count > 0:
                msg = f'Warning: This song already exists ({hash_count} hashes), skipping'
                print(colored(msg, 'yellow'))
                continue

            # Initialize an empty set to store unique hashes
            hashes = set()

            # Analyze each channel of the audio and calculate hashes
            for channeln, channel in enumerate(audio['channels']):
                channel_hashes = analyzer.fingerprint(channel, Fs=audio['Fs'])
                channel_hashes = set(channel_hashes)

                msg = f'Channel {channeln} saved {len(channel_hashes)} hashes'
                print(colored(msg, attrs=['dark']))

                # Add channel hashes to the set of unique hashes
                hashes |= channel_hashes

            # Convert unique hashes to a list of tuples for database storage
            values = [(song_id, hash, offset) for hash, offset in hashes]

            # Store the fingerprints in the database
            db.store_fingerprints(values)

    print(colored('Done', "green"))

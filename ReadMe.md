# Audio Search Engine (Shazam Clone)

**Timeline: 2021 - 2022**

This project is an Audio Search Engine built in Python that can identify music by listening to it through a microphone, much like Shazam.

## How It Works
The engine uses audio fingerprinting techniques (FFT-based spectrogram analysis) to extract distinct features from audio files.
1. **Indexing (`analyze.py`)**: The system analyzes `.wav` files in the `mp3/` directory, extracts their acoustic fingerprints, and stores the hashes in a SQLite database.
2. **Listening (`listen.py`)**: The system records audio from the microphone, fingerprints the recording on the fly, and queries the SQLite database for matches to confidently identify the song.

## Requirements
To install all required packages:
```bash
pip install -r requirement.txt
```

## Usage
1. Place your target `.wav` files in the `mp3/` folder.
2. Run `python analyze.py` to extract features and add them to the database.
3. Run `python listen.py` to start the microphone and identify playing music.

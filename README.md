# Music

A collection of useful tidal scripts.

## Music Backup

a quick way to pull your fav tracks and artists from your tidal. Never trust an online service to not loose or delete your stuff.

## Getting Started

pip install -r requirements.txt

### Running the script

cd in to the `src` dir

run `python3 tidal_export.py`

Open link that appears in console and sign in to allow script access to your account

script should only take a few seconds to run at most.

## Music Unavailable Fix

For each unavilible song in your tacks list it will find track from the same artists with excact title matches and swap them.

cd in to the `src` dir

run `python3 available_track_fixer.py`
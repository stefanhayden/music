# Music

A collection of scripts for backing up and maintaining your Tidal library.

## Setup

```bash
pip install -r requirements.txt
```

All scripts are run from the `src/` directory:

```bash
cd src
```

Authentication is handled automatically. The first time you run any script it will print an OAuth URL — open it in a browser, sign in, and grant access. Your session is saved to `.authCache.txt` so subsequent runs skip the login step.

---

## Scripts

### `tidal_export.py` — Back up your library

Exports your favorited tracks, albums, and artists to CSV files in the repo root:

| File | Contents |
|------|----------|
| `tracks.csv` | track, album, artist |
| `albums.csv` | album, artist |
| `artists.csv` | artist, id |

Also writes `missing.json` listing any favorited items that are currently unavailable on Tidal (useful as input for the restore script).

```bash
python3 tidal_export.py
```

---

### `restore_missing_tracks.py` — Re-add unavailable favorites

Reads `missing.json` (produced by `tidal_export.py`) and searches Tidal for a matching available version of each unavailable track and album. When a match is found it is added back to your favorites.

```bash
python3 tidal_export.py        # generates missing.json
python3 restore_missing_tracks.py  # searches and re-adds
```

For each item it prints whether it was `ADDED`, `NOT FOUND`, or hit an `ERROR`. Anything in the not-found list at the end needs to be re-added manually — those tracks may have been removed from Tidal entirely.

---

### `available_track_fixer.py` — Fix unavailable tracks and playlist items

Scans your favorited tracks and all of your playlists. For each unavailable track it searches the artist's top tracks for an exact title match and swaps the old unavailable version for the new one.

```bash
python3 available_track_fixer.py
```

Prints a summary of how many tracks were fixed and which artists had tracks that couldn't be replaced.

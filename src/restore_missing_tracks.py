import json
import sys
sys.path.insert(0, '..')

import tidalapi
from auth import session

with open('../missing.json') as f:
    missing = json.load(f)

favorites = tidalapi.Favorites(session, session.user.id)

def restore_tracks(tracks):
    added, not_found = [], []
    total = len(tracks)

    for i, item in enumerate(tracks):
        track_name = item["name"]
        artist_name = item["artist"]

        query = f"{track_name} {artist_name}"
        results = session.search(query, models=[tidalapi.Track], limit=10)
        candidates = results["tracks"]

        match = next(
            (t for t in candidates if t.name.lower() == track_name.lower() and t.artist.name.lower() == artist_name.lower()),
            None
        )
        if not match:
            match = next(
                (t for t in candidates if track_name.lower() in t.name.lower() and t.artist.name.lower() == artist_name.lower()),
                None
            )

        if match:
            try:
                favorites.add_track(match.id)
                print(f"[{i+1}/{total}] ADDED:     {track_name} - {artist_name}  (id:{match.id})")
                added.append(item)
            except Exception as e:
                print(f"[{i+1}/{total}] ERROR:     {track_name} - {artist_name}: {e}")
                not_found.append(item)
        else:
            print(f"[{i+1}/{total}] NOT FOUND: {track_name} - {artist_name}")
            not_found.append(item)

    return added, not_found


def restore_albums(albums):
    added, not_found = [], []
    total = len(albums)

    for i, item in enumerate(albums):
        album_name = item["name"]
        artist_name = item["artist"]

        query = f"{album_name} {artist_name}"
        results = session.search(query, models=[tidalapi.Album], limit=10)
        candidates = results["albums"]

        match = next(
            (a for a in candidates if a.name.lower() == album_name.lower() and a.artist.name.lower() == artist_name.lower()),
            None
        )
        if not match:
            match = next(
                (a for a in candidates if album_name.lower() in a.name.lower() and a.artist.name.lower() == artist_name.lower()),
                None
            )

        if match:
            try:
                favorites.add_album(match.id)
                print(f"[{i+1}/{total}] ADDED:     {album_name} - {artist_name}  (id:{match.id})")
                added.append(item)
            except Exception as e:
                print(f"[{i+1}/{total}] ERROR:     {album_name} - {artist_name}: {e}")
                not_found.append(item)
        else:
            print(f"[{i+1}/{total}] NOT FOUND: {album_name} - {artist_name}")
            not_found.append(item)

    return added, not_found


print(f"=== Restoring {len(missing['tracks'])} tracks ===")
tracks_added, tracks_failed = restore_tracks(missing["tracks"])

print(f"\n=== Restoring {len(missing['albums'])} albums ===")
albums_added, albums_failed = restore_albums(missing["albums"])

print(f"\nDone.")
print(f"Tracks  — added: {len(tracks_added)}, not found: {len(tracks_failed)}")
print(f"Albums  — added: {len(albums_added)}, not found: {len(albums_failed)}")

all_failed = {"tracks": tracks_failed, "albums": albums_failed}
total_failed = len(tracks_failed) + len(albums_failed)
if total_failed:
    print(f"\nCould not restore {total_failed} item(s):")
    for item in tracks_failed:
        print(f"  track:  {item['name']} by {item['artist']}")
    for item in albums_failed:
        print(f"  album:  {item['name']} by {item['artist']}")

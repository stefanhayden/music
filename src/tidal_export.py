# You need to install tidalapi using pip install tidalapi (more can be found here https://github.com/tamland/python-tidal)
# had to be fixed with https://github.com/tamland/python-tidal/pull/130

import json
import tidalapi

from auth import session

favorites = tidalapi.Favorites(session, session.user.id)

def cleanForCsv(val: str):
    return val.replace(',', '').replace('"', '')

missing = {"tracks": [], "albums": [], "artists": []}

#
# Get Tracks
#
with open('../tracks.csv', 'w') as f:
    f.write('track,album,artist\n')

    getMore = True
    limit = 1000
    offset = 0

    while getMore:
        tracks = favorites.tracks(limit, offset)
        offset += limit
        if len(tracks) == 0:
            getMore = False

        for track in tracks:
            f.write(','.join([cleanForCsv(track.name), cleanForCsv(track.album.name), cleanForCsv(track.artist.name)]) + '\n')
            if not track.available:
                missing["tracks"].append({"name": track.name, "album": track.album.name, "artist": track.artist.name})


#
# Get Artists
#
with open('../artists.csv', 'w') as f:
    f.write('artist,id\n')

    getMore = True
    limit = 1000
    offset = 0

    while getMore:
        artists = favorites.artists(limit, offset)
        offset += limit
        if len(artists) == 0:
            getMore = False

        for artist in artists:
            f.write(cleanForCsv(artist.name) + ',' + str(artist.id) + '\n')


#
# Get Albums
#
with open('../albums.csv', 'w') as f:
    f.write('album,artist\n')

    getMore = True
    limit = 1000
    offset = 0

    while getMore:
        albums = favorites.albums(limit, offset)
        offset += limit
        if len(albums) == 0:
            getMore = False

        for album in albums:
            f.write(','.join([cleanForCsv(album.name), cleanForCsv(album.artist.name)]) + '\n')
            if not album.available:
                missing["albums"].append({"name": album.name, "artist": album.artist.name})


with open('../missing.json', 'w') as f:
    json.dump(missing, f, indent=2, ensure_ascii=False)

print(f"Missing: {len(missing['tracks'])} tracks, {len(missing['albums'])} albums")

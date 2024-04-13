# You need to install tidalapi using pip install tidalapi (more can be found here https://github.com/tamland/python-tidal)
# had to be fixed with https://github.com/tamland/python-tidal/pull/130

import csv
import sys
import pprint
from pathlib import Path

import tidalapi

session = tidalapi.Session()

try: 
    session.load_session_from_file(Path('../.authCache.txt'))
    if session.check_login() == False:
        raise Exception('no auth saved')
except Exception:
    session.login_oauth_simple()
    session.save_session_to_file(Path('../.authCache.txt'))

favorites = tidalapi.Favorites(session, session.user.id)

#
# Get Tracks
#
open('../tracks.csv', 'w').close()
f = open("../tracks.csv", "a")

f.write('track,album,artist\n')

getMore = True
limit = 1000
offset = 0

while getMore == True:

    tracks = favorites.tracks(limit, offset);
    offset += limit;
    if len(tracks) == 0:
        getMore = False

    for track in tracks:
        f.write(','.join([track.name.replace(',', ''), track.album.name, track.artist.name]) + '\n')


#
# Get Artists
#
open('../artists.csv', 'w').close()
f = open("../artists.csv", "a")

f.write('artist\n')

getMore = True
limit = 1000
offset = 0

while getMore == True:

    artists = favorites.artists(limit, offset);
    offset += limit;
    if len(artists) == 0:
        getMore = False

    for artist in artists:
        f.write(artist.name + '\n')


#
# Get Album
#
open('../albums.csv', 'w').close()
f = open("../albums.csv", "a")

f.write('album,artist\n')

getMore = True
limit = 1000
offset = 0

while getMore == True:

    albums = favorites.albums(limit, offset);
    offset += limit;
    if len(albums) == 0:
        getMore = False

    for album in albums:
        f.write(','.join([album.name, album.artist.name]) + '\n')





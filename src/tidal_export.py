# You need to install tidalapi using pip install tidalapi (more can be found here https://github.com/tamland/python-tidal)
# had to be fixed with https://github.com/tamland/python-tidal/pull/130

import csv
import sys
import pprint

import tidalapi

session = tidalapi.Session()
session.login_oauth_simple()
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
        f.write(','.join([track.name, track.album.name, track.artist.name]) + '\n')


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




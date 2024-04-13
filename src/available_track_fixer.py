# You need to install tidalapi using pip install tidalapi (more can be found here https://github.com/tamland/python-tidal)
# had to be fixed with https://github.com/tamland/python-tidal/pull/130

import csv
import sys
import pprint
from pathlib import Path
from typing import Any, List

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
# Fix Tracks
#
def fixTracks():
    getMore = True
    limit = 1000
    offset = 0
    count  = 0;

    unavailableTracks = 0;
    fixedTracks = 0;
    unfixableArtists = set();

    while getMore == True:

        tracks = favorites.tracks(limit, offset);
        offset += limit;
        if len(tracks) == 0:
            getMore = False

        for track in tracks:
            if (track.available == False):
                unavailableTracks += 1;
                print(count, ':', track.name, ' - ', track.album.name, ' - ', track.artist.name, ' - id:', track.id);
                top_tracks = getAllTopTracks(track.artist.id)
                item = next((x for x in top_tracks if x.full_name == track.full_name), None);
                if item:
                    print('    - EXACT MATCH: ', item.id, ' - ', item.name, ' - ', item.album.name, ' - ', item.artist.name, ' - id:', item.id);
                    favorites.add_track(item.id)
                    print('            - Added new track: ', item.id)
                    favorites.remove_track(track.id)
                    print('            - Removed old unavailable track: ', track.id)
                    fixedTracks += 1;
                else:
                    unfixableArtists.add(track.artist.name)

                item = next((x for x in top_tracks if x.name == track.name), None);
                if item:
                    print('    - SHORT MATCH: ', item.id, ' - ', item.name, ' - ', item.album.name, ' - ', item.artist.name, ' - id:', item.id);

                count += 1;

    print('\nTrack Stats:')
    print('- unavailable Tracks:', unavailableTracks)
    print('- fixed Tracks:', fixedTracks)
    print('- bands with unfixable tracks:')
    for i in unfixableArtists:
        print('    - ' + i)
    print('\n')

def getAllTopTracks(artistId: str):
    getMore = True
    limit = 50
    offset = 0
    tracks = [];
    while getMore == True:
        try:
            foundTracks = session.artist(artistId).get_top_tracks(limit, offset);
        except Exception as error:
            foundTracks = [];
            pass;
        tracks = tracks + foundTracks;
        offset += limit;
        if len(foundTracks) == 0:
            getMore = False

    return tracks



#
# Fix Playlists
#
def fixPlaylists():
    playlists = session.user.playlists()
    print('playlists', len(playlists))
    playlistCount = 0;

    for playlist in playlists:
        getMore = True
        limit = 1000
        offset = 0
        print(playlistCount, ' PLAYLIST - ', playlist.name, playlist.num_tracks)
        playlistCount += 1;
        playlist.tracks(limit, offset)
        tracks: List[tidalapi.Track] | Any = [];
        while getMore == True:
            foundTracks = playlist.tracks(limit, offset);
            offset += limit;
            tracks = tracks + foundTracks;
            if len(foundTracks) == 0:
                getMore = False
        
        count = 0;
        for track in tracks:
            if (track.available == False):
                    print('\t', count, ':', track.name, ' - ', track.album.name, ' - ', track.artist.name, ' - id:', track.id);
                    top_tracks = getAllTopTracks(track.artist.id)
                    item = next((x for x in top_tracks if x.full_name == track.full_name), None);
                    if item:
                        print('\t- EXACT MATCH: ', item.id, ' - ', item.name, ' - ', item.album.name, ' - ', item.artist.name, ' - id:', item.id)
                        try:
                            playlist.add([item.id])
                            print('\t\t- ADDED: ', item.id);
                            playlist.remove_by_id(track.id);
                            print('\t\t- REMOVED: ', track.id);
                        except Exception as error:
                            print('\t\tError adding / removing', error)
                            pass;
                    count += 1;
        


fixTracks();
fixPlaylists();
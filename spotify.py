import spotipy
from spotipy.oauth2 import SpotifyOAuth


"""
PYTHON FUNCTINONS
A functions is a block of code which only runs when it's called
    You can pass data, known as parameters, into a function
    A function can return data as a result
"""
def get_spotify_playlists(username, client_id, client_secret, redirect_uri):
    #We'll need to authenticate this with the info from the spotify API dashboard
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private',
        username=username
    ))

    #SpotiPy docs state that this is used to get current users playlists. SpotiFy api examples show that the json contains a list of items, hence my return statement
    playlists = sp.current_user_playlists()

    return playlists['items']

#Need to create playlist with fifa tracks implemented
def create_playlist_with_fifa_tracks(username, client_id, client_secret, redirect_uri):
    #Get my playlists using the 1st function
    playlists = get_spotify_playlists(username, client_id, client_secret, redirect_uri)

    #We'll need to authenticate this with the info from the spotify API dashboard. Scopes listed from spotify API docs
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private',
        username=username
    ))

    # Creates a new playlist to my user id (name) and named fifa playlists
    new_playlist = sp.user_playlist_create(username, name='FIFA songs')

    #Loop through my playlists and add tracks to the new fifa playlist
    for playlist in playlists:
        #Checks for FIFA in playlist name, adds tracks from each playlis
        if 'FIFA' in playlist['name']:
            #Looks for track id (id is needed to add tracks to playlist)
            tracks = sp.playlist_tracks(playlist['id'])
            #need empty array to place the findings
            track_uris = []
            #nested for loop that will add the fifa playlist tracks to its own master playlist
            for track in tracks['items']:
                #Captures all uris and appends it to that empty list
                track_uri = track['track']['uri']
                track_uris.append(track_uri)

            #Since the array now contains the appropiate data, this can be used to add our uris to the new playlist
            sp.playlist_add_items(new_playlist['id'], track_uris)

    #This uses f string to print out a confirmation msg
    print(f"Playlist '{new_playlist['name']}' created with tracks from Aaron's FIFA playlists.")

#Needed for auth, setup on official spotify api
client_id = 'fda2419b941641f1945008c815659427'
client_secret = 'ab7680a3f94f457db72552314a41787e'
redirect_uri = 'http://localhost:3000/artist-search'
username = '12181686267'

#Runs the function and passed our auth arguments
create_playlist_with_fifa_tracks(username, client_id, client_secret, redirect_uri)
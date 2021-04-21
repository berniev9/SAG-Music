import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3
import unittest

#log in credentials
cid = '2d7d29fc683a48b7849fb37a344f32a0'
secret = '0a3b0853f43f4b8e9ba53ae0b4edf794'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)


# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'
#https://api.spotify.com/v1/user/b0ffdb7013d2429d
# SpotifyCharts ID from the URI - https://open.spotify.com/user/spotifycharts?si=b0ffdb7013d2429d
#spotifycharts_id = 'b0ffdb7013d2429d'
Token = "BQAaCsH_oQPQFfrOhSSx2TiEGsms4V0p8MCLhJKjV5hJeRMsTR6CAlKNmsARYguvSFvvT98NfBUjhf5P8CoNIx-FadI1aCbTi6bApr8YdlWJqh6guk-iQ-ea6hkbYGgkJoVvq-tgxlUB9294"

#FIND OUT HOW TO AUTHENTIC PERMANENT TOKEN!!!^^^^^^^^^^

def setUpDatabase(db_name): #should be good
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn): #needs adjustments
    cur.execute('CREATE TABLE IF NOT EXISTS Spotify (Song TEXT, Artist Text') #add more columns on table
    conn.commit()

def songsearchinfo(song):
    url = "https://api.spotify.com/v1/search"

    queryparameters = {"q":song,"type":"track","limit":"5"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }
    
    response = requests.request("GET", url, headers=Headers, params=queryparameters)

    data = response.text
    jdata = json.loads(data)
    print(jdata)


def songsearchgetid(song):
    """Retrieves the artists' id from the title of the song on the billboard 100 list"""
    url = "https://api.spotify.com/v1/search"

    queryparameters = {"q":song,"type":"track","limit":"5"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }
    
    response = requests.request("GET", url, headers=Headers, params=queryparameters)

    data = response.text
    jdata = json.loads(data)
    selectedinfo = []
    artist = jdata["tracks"]["items"][0]["artists"][0]["name"]
    artistid = jdata["tracks"]["items"][0]["artists"][0]["id"]
    for info in (artist, artistid):
        selectedinfo.append(info)
    print(selectedinfo)
    print("Artist name - " + artist + ", Artist ID - " + artistid)
    return artistid

def breakoutsongforartist(song, market = "US"):
    """Returns if the song is a breakout song for the artist based off of the performance of their prior songs"""
    artistid = songsearchgetid(song)

    url = "https://api.spotify.com/v1/artists/"#{id}/top-tracks"
    #queryparameters = {"{id}":artistid,"market":"US"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }

    response = requests.request("GET", url + str(artistid) + "/top-tracks?market=" + market, headers=Headers)#, params=queryparameters)
    data = response.text
    jdata = json.loads(data)
    
    #prints out top songs
    for songrank in range(len(jdata["tracks"])):
        print(jdata["tracks"][songrank]['name'])

    #prints out popularity
    for songrank in range(len(jdata["tracks"])):
        print(jdata["tracks"][songrank]['popularity'])
    popularities = []
    average = 0
    for songrank in range(len(jdata["tracks"])):
        popularities.append((jdata["tracks"][songrank]['popularity']))
    #print(popularities)
    for popularity in popularities:
        average += popularity
    #print(average)
    average= average/len(popularities)
    print(average)

    #DETERMINE IF SONG IS MORE POPULAR THAN AVERAGE
#get song from Jacob's beautsoup
#breakoutsongforartist("No Hands")
songsearchinfo("I'll Find You")


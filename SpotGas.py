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
Token = "BQBTZhswo0NdM-hx1pB3oxiNhep5sUzDPorWzL9FLlpyUMKoLv6Ihl7QT7vLW-Zb9T5mE0JgJvvDk7SDHOEjb_wKDP-xJSfuoNRv1VdTYo-uK6C3f5zEQvxV0OopyIlurNdmvatfDKAldxc9"

#FIND OUT HOW TO AUTHENTIC PERMANENT TOKEN!!!^^^^^^^^^^

def setUpDatabase(db_name): #should be good
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn): #needs adjustments
    cur.execute('CREATE TABLE IF NOT EXISTS Spotify (Song TEXT, Artist Text, Popularity Integer Popularity_Status Integer') #Popularity Status is 1-4 and synonymous with __calculatedbreakout__ in doc plan
    conn.commit()

def songsearchinfo(song):
    """Returns JSON song search data from Spotify"""
    url = "https://api.spotify.com/v1/search"

    queryparameters = {"q":song,"type":"track","limit":"5"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }
    
    response = requests.request("GET", url, headers=Headers, params=queryparameters)

    data = response.text
    jdata = json.loads(data)
    return(jdata)

def songsearchgetartist(song):
    """Retrieves the artist name from the song on the billboard 100 list"""

    searchresults = songsearchinfo(song)
    artist = searchresults["tracks"]["items"][0]["artists"][0]["name"]
    return artist

def songsearchgetid(song):
    """Retrieves the artists' ID from the title of the song on the billboard 100 list"""
    
    searchresults = songsearchinfo(song)
    artist = songsearchgetartist(song)
    artistid = searchresults["tracks"]["items"][0]["artists"][0]["id"]
    return artistid

def songsearchgetpopularity(song):
    """Retrieves the popularity of a song"""
    searchresults = songsearchinfo(song)
    popularity = searchresults["tracks"]["items"][0]["popularity"]
    return popularity

def toptracksartistdata(song, market = "US"):
    """Returns the top tracks of the artist of the inputted song in the form of JSON data"""
    artistid = songsearchgetid(song)

    url = "https://api.spotify.com/v1/artists/"
    
    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }

    response = requests.request("GET", url + str(artistid) + "/top-tracks?market=" + market, headers=Headers)
    data = response.text
    jdata = json.loads(data)
    return jdata

def toptracksartistlist(song, market = "US"):
    """Returns a list of the top 10 songs from the same artist who made another song"""
    toptrackdata = toptracksartistdata(song, market)
    topsongs = []
    for songrank in range(len(toptrackdata["tracks"])):
        topsongs.append((toptrackdata["tracks"][songrank]['name']))
    return topsongs
    
def meanartistpopularity(song, market = "US", popularratings = False):
    """Calculates the average popularity of the artist's top 10 songs and can print out Spotify popularity ratings for those songs"""
    topsongdata = toptracksartistdata(song, market)
    if popularratings == True:
        for songrank in range(len(topsongdata["tracks"])):
            print(topsongdata["tracks"][songrank]['popularity'])
    popularities = []
    average = 0
    for songrank in range(len(topsongdata["tracks"])):
        popularities.append((topsongdata["tracks"][songrank]['popularity']))
    for popularity in popularities:
        average += popularity
    average= average/len(popularities)
    return average

def breakoutsongforartist(song, market = "US"):
    """Determines if a song is a "Breakout Song" for the artist"""
    if meanartistpopularity(song) >= 65:
        if songsearchgetpopularity(song)>=meanartistpopularity(song):
            return "This artist is already popular, and this song is only adding to that!"
        else:
            return "This artist is popular, but this isn't even one of their hottest songs!"
    if meanartistpopularity(song)<= 65:
        if songsearchgetpopularity(song) >= meanartistpopularity(song):
            return "This is a breakout song for the artist!"
        else:
            return "This song is just as good as their other top songs!"

#get song from Jacob's beautsoup
#for item in ["Sweater Weather", "Tell Me Why (Taylor's Version)", "On Me", "Back in Blood", "deja vu"]:
    #print(breakoutsongforartist(item))

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
Token = "BQA7QHe_r1s36_91gpMM8yPI2zI_FHwyut2LU88NDCkpWt81kaOcsCf7Gj4AAafJr_6PuBa1Zp3wkliwcIz0-hw8EWD3u5BvgDcOJfhMqeKZlb-kTWdxE6u_thDG7tLztqmLVbCfT7_M_V_G"

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
    """Returns JSON song search data from Spotify"""
    url = "https://api.spotify.com/v1/search"

    queryparameters = {"q":song,"type":"track","limit":"5"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }
    
    response = requests.request("GET", url, headers=Headers, params=queryparameters)

    data = response.text
    jdata = json.loads(data)
    #print(jdata)
    return(jdata)


def songsearchgetid(song):
    """Retrieves the artists' id from the title of the song on the billboard 100 list"""
    
    searchresults = songsearchinfo(song)
    selectedinfo = []
    artist = searchresults["tracks"]["items"][0]["artists"][0]["name"]
    artistid = searchresults["tracks"]["items"][0]["artists"][0]["id"]
    for info in (artist, artistid):
        selectedinfo.append(info)
    print(selectedinfo)
    print("Artist name - " + artist + ", Artist ID - " + artistid)
    return artistid

def songsearchgetpopularity(song):
    """Retrieves the popularity of a song"""
    searchresults = songsearchinfo(song)
    #print(searchresults["tracks"]["items"][0]["popularity"])
    popularity = searchresults["tracks"]["items"][0]["popularity"]
    return popularity

def toptracksartistdata(song, market = "US"):
    """Returns the top tracks of the artist of the inputted song"""
    artistid = songsearchgetid(song)

    url = "https://api.spotify.com/v1/artists/"#{id}/top-tracks"
    #queryparameters = {"{id}":artistid,"market":"US"}

    Headers =  {
        'Authorization': 'Bearer {token}'.format(token=Token)
        }

    response = requests.request("GET", url + str(artistid) + "/top-tracks?market=" + market, headers=Headers)#, params=queryparameters)
    data = response.text
    jdata = json.loads(data)
    return jdata

def toptracksartistlist(song, market = "US"):
    toptrackdata = toptracksartistdata(song, market)
    topsongs = []
    #returns top songs
    for songrank in range(len(toptrackdata["tracks"])):
        topsongs.append((toptrackdata["tracks"][songrank]['name']))
    return topsongs
    
def meanartistpopularity(song, market = "US"):
    #prints out popularity
    topsongdata = toptracksartistdata(song, market)
    for songrank in range(len(topsongdata["tracks"])):
        print(topsongdata["tracks"][songrank]['popularity'])
    popularities = []
    average = 0
    for songrank in range(len(topsongdata["tracks"])):
        popularities.append((topsongdata["tracks"][songrank]['popularity']))
    #print(popularities)
    for popularity in popularities:
        average += popularity
    #print(average)
    average= average/len(popularities)
    #print(average)
    return average

def breakoutsongforartist(song, market = "US"):
    #DETERMINE IF SONG IS MORE POPULAR THAN AVERAGE"""
    if songsearchgetpopularity(song) >= meanartistpopularity(song):
        return "This is a breakout song for the artist!"
    else:
        return "This artist is typically popular and this song follows suit!"
#get song from Jacob's beautsoup
#breakoutsongforartist("No Hands")
#print(songsearchgetid("I'll Find You"))
print(breakoutsongforartist("Tell Me Why (Taylor's Version)"))

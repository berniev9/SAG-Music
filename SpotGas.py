import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3
import unittest
import os
from Shazamapi import *
from Billboard_top_100 import * 


#log in credentials
cid = '2d7d29fc683a48b7849fb37a344f32a0'
secret = '0a3b0853f43f4b8e9ba53ae0b4edf794'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)



def create_Spotify_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Spotify (Rank INTEGER, Song TEXT, Artist TEXT, Popularity INTEGER, Popularity_Status INTEGER)') #Popularity Status is 1-4 and synonymous with __calculatedbreakout__ in doc plan
    conn.commit()

    tableid = None
    cur.execute('SELECT max(Rank) FROM Spotify')
    try:
        row = cur.fetchone()
        if row is None:
            tableid = 0
        else:
            tableid = row[0]
    except:
        tableid = 0
    if tableid is None:
        tableid = 0
    
    rank = tableid + 1

    cur.execute("SELECT Song FROM Billboard")
    songdata = []
    rows = cur.fetchall()
    count = 0
    for item in rows[tableid:]:
        songdata.append(combinedata(item[0]))
        count += 1
        if count == 25:
            break

    for item in songdata:
        song = item[0].upper()
        artist = item[1]
        popularity = item[2]
        popularity_status = item[3]
        cur.execute("INSERT INTO SPOTIFY (Rank, Song, Artist, Popularity, Popularity_Status) VALUES (?, ?, ?, ?, ?)", (rank, song, artist, popularity, popularity_status))
        conn.commit()
        rank += 1
    conn.commit()

def songsearchinfo(song):
    """Returns JSON song search data from Spotify"""
    data = sp.search(song)
    return(data)

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
    toptracks = sp.artist_top_tracks(artistid, market)
    return toptracks

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

def combinedata(song):
    """Combines data of song for storage in database. 1 represents a breakout song, 2 represents a new popular song by a popular artist, 3 represents a popular"""
    song = song
    artist = songsearchgetartist(song)
    popularity = songsearchgetpopularity(song)
    if breakoutsongforartist(song) == "This is a breakout song for the artist!":
        breakout = 1
    elif breakoutsongforartist(song) == "This artist is already popular, and this song is only adding to that!":
        breakout = 2
    elif breakoutsongforartist(song) == "This artist is popular, but this isn't even one of their hottest songs!":
        breakout = 3
    elif breakoutsongforartist(song) == "This song is just as good as their other top songs!":
        breakout = 4
    datatup = (song, artist, popularity, breakout)
    return datatup




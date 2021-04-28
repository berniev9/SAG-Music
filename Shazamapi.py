import requests
import json
import sqlite3			
import os
import unittest
from Billboard_top_100 import * 
from SpotGas import *


#Functions Grabs the top 100 track that have been Shazamed this week
def top_100_songs(Country_code):

    #Shazam API
    url = "https://shazam-core.p.rapidapi.com/v1/charts/country"

    querystring = {"country_code":Country_code,"limit":"100" }

    headers = {
        'x-rapidapi-key': "777245208fmshb0a2322bac9c61cp1109b4jsn583c58319591",
        'x-rapidapi-host': "shazam-core.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.text

    #turns text into a list
    dic_list = json.loads(data)
    new_list = [] 

    rank = 1
    #Appends into a list, a tuple with the title of the song, artists, and the rank the song is on the board
    for i in dic_list:
        #Tuple = (Song, list of artists, rank)
        tuple = (i['title'], get_artists(i['artists']), rank)
        new_list.append(tuple)
        rank+=1
    return new_list

#Function takes in a list of artist and checks to see if there are any.
# If none, then the artist is set as unknown
def get_artists(artists):
    new_list = []
    #Checks to see if artist is empty
    if artists != None:
        # Iterates and adds all the artits to a list
        for follow in artists:
            new_list.append(follow['alias'])
        return new_list
    else:
        # If empty the artist is just set as Unknown
        new_list.append('Unknown')
        return new_list



# Counts the amount of times the artist appears on the top 100 Shazamed Songs
# Returns a list of tuples with the artist name and amount of times they aappear 
def get_count_artists_appear(US_top100):
    artist_list = {}
    # Iterates through a list 
    for song in US_top100:
        # Iterates through a tuple
        for art in song[1]:
            # Checks to see if the artist is already in the dict 
            if not art in artist_list.keys():
                artist_list[art] = 1
            # if not they are added in with a value of 1
            else:
                artist_list[art] = artist_list[art] + 1

    # Sorts the list by the highest amount of times the artist appears on the board
    ranked = sorted(artist_list.items(),key= lambda t: t[1], reverse=True)

    return ranked

# Calculations
# Calculates the frequency the artist shows up from the 100 top Shazamed Songs of the week
# Returns a dict with the key as the artist name, and value as the frequency
def calculate_artist_frequency(artist_rank_list):
    dict = {}
    for art in artist_rank_list:
        dict[art[0]] = art[1]/100

    return dict


# Takes in a artist and the top 100 Shazamed Songs
def get_artist_pop_song(artist,US_top100):
    # Loops through the US_top100 list and finds the 
    # first instance that the artist appears in
    for song in US_top100:
        for art in song[1]:
            if artist == art:
                # returns the most popular song of that artist
                return song[0]

# Creates and adds the Shazam data table into the database
# Holds basic info that the API provides
# Takes in cur, conn and a list of tuples with the song, artist =[], rank on the board
def create_Shazam_table(cur,conn, US_top100):
    cur.execute('CREATE TABLE IF NOT EXISTS Shazam_Data (Rank_of_song INTEGER PRIMARY KEY, Song TEXT, Artists TEXT)')
    ### Picks up where we left off
    start_id = None
    cur.execute('SELECT max(Rank_of_song) FROM Shazam_Data')
    try:
        row = cur.fetchone()
        if row is None:
            start_id = 0
        else:
            start_id=row[0]
    except:
        start_id = 0
    if start_id is None:
        start_id = 0
 
    ####
    count = 0
    # limits the amount of data being stored into the database by 25
    while count < 25: 
        # Creates a string of all the artists who are in the song
        art = ''
        for i in US_top100[start_id][1]:
            art = art + i + ', '
        # Inserts one at a time the Rank, Song, and Artists in the song
        cur.execute("INSERT OR IGNORE INTO Shazam_Data (Rank_of_song, Song, Artists)  VALUES (?,?,?)", (int(US_top100[start_id][2]),US_top100[start_id][0].upper(), art))
        conn.commit()
        start_id+=1
        count+=1
    conn.commit()


# Creates and adds the Shazam data table into the database this time with calculated data
# Takes in cur, conn and a dictionary with the artist name and their frequency 

def create_calculate_shazam_table(cur,conn, dictionary, US_top100):
    cur.execute('CREATE TABLE IF NOT EXISTS Shazam_calculated_data (Rank_for_most_popular_artist INTEGER PRIMARY KEY, Artist TEXT, Artist_most_popular_song TEXT, Frequency_the_artist_appears REAL)')
     ### Picks up where we left off
    start_id = None
    cur.execute('SELECT max(Rank_for_most_popular_artist) FROM Shazam_calculated_data')
    try:
        row = cur.fetchone()
        if row is None:
            start_id = 0
        else:
            start_id=row[0]
    except:
        start_id = 0
    if start_id is None:
        start_id = 0
    ####
    count = 0
    key_list = []
    # Created a list of artists to easy input into the database
    for key in dictionary.keys():
        key_list.append(key)
    # limits the amount of data being stored into the database by 25
    while count < 25:
        #Checks to see if start_id will be out of the scope
        if start_id+1 != 100:
            cur.execute("INSERT OR IGNORE INTO Shazam_calculated_data (Rank_for_most_popular_artist, Artist, Artist_most_popular_song, Frequency_the_artist_appears)  VALUES (?,?,?,?)",(start_id+1,key_list[start_id],get_artist_pop_song(key_list[start_id], US_top100), dictionary[key_list[start_id]]))
            conn.commit()
            start_id+=1
            count+=1
        else:
            count+=1
            continue
    conn.commit()




import requests
import re
import os
import csv
import unittest
import sqlite3

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def dataprocess(cur, conn):
    cur.execute('SELECT Billboard.Song, Billboard.Rank, Spotify.Popularity, Shazam_Data.Rank_of_song FROM Billboard JOIN Spotify on Billboard.Song = Spotify.Song JOIN Shazam_Data on BillBoard.Song = Shazam_Data.Song')
    rows = cur.fetchall()
    ranking_list = []
    for item in rows:
        song = item[0]
        billboard = item[1]
        spotify = 101 - item[2] # this makes an assumption that popularity from Spotify can be equated to the ranking of the other api/website. this relationship in reality is unknown but it does provide insight into the verying degrees of "popularity" of the songs across platforms
        shazam = item[3]
        avg = (billboard + spotify + shazam)/3
        tup = (song, int(avg)) #use int to round down to nearest whole number.
        ranking_list.append(tup)
    ranking_list.sort(key = lambda x: x[1])
    return ranking_list

def writetotext(cur, conn, text_name):
    data = dataprocess(cur, conn)
    with open(text_name, 'w') as f:
        f.write('Below is the average "popularity" out of 100 total of a song between Spotify, Billboard, and Shazam.')
        f.write('\n')
        f.write('A value of one is the most popular and a value of 100 is the least popular.')
        for item in data:
            f.write('\n')
            f.write(f"{item[0]} ---- {item[1]}")
        
            
        

def main():
    cur, conn = setUpDatabase('GAS_MEDIA.db')
    writetotext(cur, conn, 'ProcessedData.txt')
if __name__ == "__main__":
    main()
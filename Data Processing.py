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
    print(len(rows))
    for item in rows:
        print(item)

def main():
    cur, conn = setUpDatabase('GAS_MEDIA.db')
    dataprocess(cur, conn)
if __name__ == "__main__":
    main()
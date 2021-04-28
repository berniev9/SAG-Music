from bs4 import BeautifulSoup
import requests
import json
import sqlite3			
import os
import unittest
import re
import csv
from Shazamapi import *
from Billboard_top_100 import * 
from SpotGas import *




def main():

    cur, conn = setUpDatabase('GAS_MEDIA.db')
    

    
    #Billboard 
    billboard_table('2021', '04', '10', 'GAS_MEDIA.db')


    #Shazam 
    #Goes through api to create a list of tuples that includes (song, list of artists, Rank on the Shazam board)
    US_100mostshazam_songs = top_100_songs('US')
    # Creates a list of tuples that includes the individual artist name the amount of times they appear on the top 100 shazamed songs
    artist_rank = get_count_artists_appear(US_100mostshazam_songs)
    # Creates a dict that holds the artist name as the key and the frequency as the value
    frequency = calculate_artist_frequency(artist_rank)
    # Creates a connection to the databse 
    # Adds API info onto the database
    create_Shazam_table(cur, conn,US_100mostshazam_songs)
    # Adds calculated info onto the database
    create_calculate_shazam_table(cur,conn, frequency, US_100mostshazam_songs)

    # Spotify
    create_Spotify_table(cur, conn)


if __name__ == "__main__":
    main()

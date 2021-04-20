
#this will use beautiful soup to scrape the billboard top 100 for the most popular songs world wide.

from bs4 import BeautifulSoup
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

def create_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Billboard (Rank INTEGER PRIMARY KEY, Song TEXT, Artist TEXT, Previous_Rank INTEGER, Peak_Rank INTEGER, Weeks_on_Charts INTEGER)')
    conn.commit()
    

def billboard_soup(year, month, day):
    cur, conn = setUpDatabase('GAS_MEDIA.db')  

    create_table(cur, conn)

    partial_url = 'https://www.billboard.com/charts/hot-100/'
    updated_url = partial_url + str(year) + '-' + str(month) + '-' + str(day)

    r = requests.get(updated_url)
    if r.ok:
        soup = BeautifulSoup(r.content, 'html.parser')

    anchor = soup.find_all('col', class_ = 'chart-list__elements')
    i = 0
    while i < 26:
        for item in anchor:
            rank = item.find('span', class_ = 'chart-element__rank__number')
            song = item.find('span', class_ = 'chart-element__information__song text--truncate color--primary')
            artist = item.find('span', class_ = 'chart-element__information__artist text--truncate color--secondary')
            previous_rank = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--last')
            peak_rank = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--peak')
            wks_on_chart = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--week')
            print([rank, song, artist, previous_rank, peak_rank, wks_on_chart])
            cur.execute(f"SELECT Song FROM Billboard")
            rows = cur.fetchall()
            if song not in rows:
                cur.execute("INSERT INTO Billboard (Rank, Song, Artist, Previous Rank, Peak Rank, Weeks on Charts) VALUES (?,?,?,?,?,?)",(rank,song,artist,previous_rank, peak_rank,wks_on_chart))
                conn.commit()
                i += 1
            else:
                continue

billboard_soup('2021', '04', '10')


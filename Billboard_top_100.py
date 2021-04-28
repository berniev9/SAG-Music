#this will use beautiful soup to scrape the billboard top 100 for the most popular songs world wide.

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import sqlite3
from Shazamapi import *
from SpotGas import *


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Billboard (Rank INTEGER PRIMARY KEY, Song TEXT, Artist TEXT, Previous_Rank INTEGER, Peak_Rank INTEGER, Weeks_on_Charts INTEGER)')
    conn.commit()
    

def billboard_soup(year, month, day):
    partial_url = 'https://www.billboard.com/charts/hot-100/'
    updated_url = partial_url + str(year) + '-' + str(month) + '-' + str(day)
    print(updated_url)
    r = requests.get(updated_url)
    if r.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
    empty_list = []
    anchor = soup.find('ol', class_ = 'chart-list__elements')
    anchor2 = anchor.find_all('li', class_ = 'chart-list__element display--flex')
    for item in anchor2:
        rank = item.find('span', class_ = 'chart-element__rank__number').get_text().strip()
        song = item.find('span', class_ = 'chart-element__information__song text--truncate color--primary').get_text().strip()
        artist = item.find('span', class_ = 'chart-element__information__artist text--truncate color--secondary').get_text().strip()
        previous_rank = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--last').get_text().strip()
        peak_rank = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--peak').get_text().strip()
        wks_on_chart = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--week').get_text().strip()
        tup = (rank, song, artist, previous_rank, peak_rank, wks_on_chart)
        empty_list.append(tup)
    return empty_list


def billboard_table(year, month, day, db_name):

    cur, conn = setUpDatabase(db_name)

    create_table(cur, conn)

    billboard_data = billboard_soup(year, month, day)

    i = 0

    #Bernies solution for entering 25 at a time
    start_id = None
    cur.execute('SELECT max(rank) FROM Billboard')
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


    for item in billboard_data[start_id:]:
        #cur.execute(f"SELECT Song FROM Billboard")
        #rows = cur.fetchall()
        #song = item[1]
        #if song not in rows:
        cur.execute("INSERT INTO Billboard (Rank, Song, Artist, Previous_Rank, Peak_Rank, Weeks_on_Charts) VALUES (?,?,?,?,?,?)",(item[0],item[1].upper(),item[2],item[3], item[4], item[5]))
        i +=1
        conn.commit()
        if i == 25:
            break
    


# def main():
#     #cur, conn = setUpDatabase('GAS_MEDIA.db')  
#     #create_table(cur, conn)
#     #print(billboard_soup('2021', '04', '10'))
#     billboard_table('2021', '04', '10', 'GAS_MEDIA.db')
# if __name__ == "__main__":
#     main()
    
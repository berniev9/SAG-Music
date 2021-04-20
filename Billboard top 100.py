#this will use beautiful soup to scrape the billboard top 100 for the most popular songs world wide.

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

def billboard_soup(year, month, day):
    partial_url = 'https://www.billboard.com/charts/hot-100/'
    updated_url = partial_url + str(year) + '-' + str(month) + '-' + str(day)
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
    empty_list = []
    anchor = soup.find_all('col', class_ = 'chart-list__elements')
    while i < 26:
        for item in anchor:
            rank = item.find('span', class_ = 'chart-element__rank__number')
            song = item.find('span', class_ = 'chart-element__information__song text--truncate color--primary')
            artist = item.find('span', class_ = 'chart-element__information__artist text--truncate color--secondary')
            previous_rank = item.find('span', class_ = 'chart-element__meta text--center color--secondary text--last')

    
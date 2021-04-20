import requests
import json
import sqlite3			
import os
import unittest


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def top_25songs_city(city_id):
    url = "https://shazam-core.p.rapidapi.com/v1/charts/city"

    querystring = {"city_id":city_id,"limit":"25"}

    headers = {
        'x-rapidapi-key': "777245208fmshb0a2322bac9c61cp1109b4jsn583c58319591",
        'x-rapidapi-host': "shazam-core.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.text
    dic_list = json.loads(data)

    # dict_keys(['id', 'type', 'layout', 'title', 'url', 'apple_music_url', 'subtitle', 'images', 'share', 'hub', 'artists'])
    new_list = [] 

    for i in dic_list:
        tuple = (i['title'], i['subtitle'])
        new_list.append(tuple)

    return new_list


def create_city_playlist(empty_dic, top_US_cities):
    for city in top_US_cities.keys():
        list = top_25songs_city(top_US_cities[city])
        empty_dic[city] = list

    return empty_dic


def create_database(cur, conn,dictionary):
    cur.execute('DROP TABLE IF EXISTS Shazam datatable')
    # stuck on what I will put into the database city, .....
    cur.execute('CREATE TABLE IF NOT EXISTS Shazam datatable ("City" TEXT PRIMARY KEY, "wins" INTEGER)')
    conn.commit()
    for key in dictionary.keys():
        cur.execute("INSERT OR IGNORE INTO tennis (name, wins)  VALUES (?,?)", (key, dictionary[key]))
    conn.commit()



def main():

    top_US_cities = { "Boston, Ma": "4930956" ,  "Chicago, Il": '4887398', "Las Vegas, Ne": "5506956", "Los Angeles, Ca" : "5368361", "Miami, Fl": "4164138","New York City, Ny": "5128581", "San Diego, Ca": "5391811", "San Francisco, Ca": "5391959","San Jose, Ca": "5392171", "Washington, DC": "4140963" }
    city_playlist = {}
    # Creates a dictionary that contains the city as the key , a playlist list as the value
    # with the top 25 songs of that area, a tuple with artist and their song.city_playlist

    # opinion are we looking at aritst or song, if we are doing artist
    city_playlist = create_city_playlist(city_playlist, top_US_cities)
    cur, conn = setUpDatabase('Mainmusicdatabase.db')
    


if __name__ == "__main__":
    main()
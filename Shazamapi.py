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



# def create_database(cur, conn,dictionary):
#     cur.execute('DROP TABLE IF EXISTS Shazam datatable')
#     # stuck on what I will put into the database city, .....
#     cur.execute('CREATE TABLE IF NOT EXISTS Shazam datatable ("City" TEXT PRIMARY KEY, "wins" INTEGER)')
#     conn.commit()
#     for key in dictionary.keys():
#         cur.execute("INSERT OR IGNORE INTO tennis (name, wins)  VALUES (?,?)", (key, dictionary[key]))
#     conn.commit()


#     # cur, conn = setUpDatabase('Mainmusicdatabase.db')
    



def top_100_songs(Country_code):

    url = "https://shazam-core.p.rapidapi.com/v1/charts/country"

    querystring = {"country_code":Country_code,"limit":"100" }

    headers = {
        'x-rapidapi-key': "777245208fmshb0a2322bac9c61cp1109b4jsn583c58319591",
        'x-rapidapi-host': "shazam-core.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.text
    # dict_keys(['id', 'type', 'layout', 'title', 'url', 'apple_music_url', 'subtitle', 'images', 'share', 'hub', 'artists'])
    dic_list = json.loads(data)
    new_list = [] 

    rank = 1
    for i in dic_list:
        tuple = (i['title'], get_artists(i['artists']), rank)
        new_list.append(tuple)
        rank+=1
    return new_list


def get_artists(artists):
    new_list = []
    if artists != None:
        for follow in artists:
            new_list.append(follow['alias'])
        return new_list
    else:
        new_list.append('Unknown')
        return new_list


def get_artistsand_appear(top_songs):
    artist_list = {}
    for song in top_songs:
        for art in song[1]:
            if not art in artist_list.keys():
                artist_list[art] = 1
            else:
                artist_list[art] = artist_list[art] + 1

    ranked = sorted(artist_list.items(),key= lambda t: t[1], reverse=True)

    return ranked

def calculate_artist_frequency(artist_rank_list, length):
    dict = {}
    for art in artist_rank_list:
        dict[art[0]] = art[1]/length

    return dict


def main():
    US_100mostshazam_songs = top_100_songs('US')
    artist_rank = get_artistsand_appear(US_100mostshazam_songs)
    frequency = calculate_artist_frequency(artist_rank, len(US_100mostshazam_songs))
    # print(frequency)


if __name__ == "__main__":
    main()
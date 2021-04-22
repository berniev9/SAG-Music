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
        new_list.append('Vedo')
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

def calculate_artist_frequency(artist_rank_list):
    dict = {}
    for art in artist_rank_list:
        dict[art[0]] = art[1]/100

    return dict


def get_artist_pop_song(artist,US_top100):
    for song in US_top100:
        for art in song[1]:
            if artist == art:
                return song[0]


def create_Shazam_table(cur,conn, US_top):
    cur.execute('CREATE TABLE IF NOT EXISTS Shazam_Data (Rank_id INTEGER PRIMARY KEY, Song TEXT, Artists TEXT)')
    start_id = None
    cur.execute('SELECT max(Rank_id) FROM Shazam_Data')
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
 

    count = 0
    while count < 25: 
        art = ''
        for i in US_top[start_id][1]:
            art = art + i + ', '
        cur.execute("INSERT OR IGNORE INTO Shazam_Data (Rank_id, Song, Artists)  VALUES (?,?,?)", (int(US_top[start_id][2]),US_top[start_id][0], art))
        conn.commit()
        start_id+=1
        count+=1
    conn.commit()





def create_calculate_shazam_table(cur,conn, dictionary, US_top):
    cur.execute('CREATE TABLE IF NOT EXISTS Shazam_calculated_data (Rank INTEGER PRIMARY KEY, Artist TEXT, Most_Popular_Song TEXT, Frequency_the_artist_appears REAL)')
    start_id = None
    cur.execute('SELECT max(Rank) FROM Shazam_calculated_data')
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
 
    count = 0
    key_list = []
    for key in dictionary.keys():
        key_list.append(key)


    # if start_id >=75:
        # while count < len(dictionary):
        #     print(start_id )
        #     cur.execute("INSERT OR IGNORE INTO Shazam_calculated_data (Rank, Artist, Most_Popular_Song, Frequency_the_artist_appears)  VALUES (?,?,?,?)", (start_id+1,key_list[start_id],get_artist_pop_song(key_list[start_id], US_top), dictionary[key_list[start_id]]))
        #     conn.commit()
        #     start_id+=1
        #     count+=1
        # conn.commit()
    # else:
    while count < 25:
        if start_id+1 != 100:
            cur.execute("INSERT OR IGNORE INTO Shazam_calculated_data (Rank, Artist, Most_Popular_Song, Frequency_the_artist_appears)  VALUES (?,?,?,?)", (start_id+1,key_list[start_id],get_artist_pop_song(key_list[start_id], US_top), dictionary[key_list[start_id]]))
            conn.commit()
            start_id+=1
            count+=1
        else:
            continue
    conn.commit()



def main():
    US_100mostshazam_songs = top_100_songs('US')
    artist_rank = get_artistsand_appear(US_100mostshazam_songs)
    frequency = calculate_artist_frequency(artist_rank)
    cur, conn = setUpDatabase('GAS_MEDIA.db')
    # cur.execute('DROP TABLE IF EXISTS Shazam_Data')
    create_Shazam_table(cur, conn,US_100mostshazam_songs)
    # cur.execute('DROP TABLE IF EXISTS Shazam_Data')
    # cur.execute('DROP TABLE IF EXISTS Shazam_calculated_data')
    create_calculate_shazam_table(cur,conn, frequency, US_100mostshazam_songs)
    # cur.execute('DROP TABLE IF EXISTS Shazam_calculated_data')



if __name__ == "__main__":
    main()
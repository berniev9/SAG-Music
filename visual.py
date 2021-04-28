import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Creates a dictionary with the key being the frequency and the value is the amount of times that a frequency appears
def grabs_shazam_data(cur, conn):
    cur.execute('SELECT * FROM Shazam_calculated_data')
    database = cur.fetchall()

    new_dic = {}
    #Iterates through the list to count the amount of times the freuquency appears
    for song in database:
        if not song[3] in new_dic.keys():
            new_dic[song[3]] = 1
        else:
            new_dic[song[3]]+=1

    data = sorted(new_dic.items(),key= lambda t: t[1], reverse=True)
    return data

# Creates the main shazam visual
def create_shazam_visual(data):
    # Type of frequency
    frequency = []
    # Number of artists with a type of frequency
    num_artists = []

# Creates the lists that will be inserted to make the visual
    for song in data:
        frequency.append(float(song[0]))
        num_artists.append(int(song[1]))

    layout1 = go.Layout(
        title="Number of Frequencies on the top 100 Shazamed song",
        xaxis=dict(
            title="Frequencies"
        ),
        yaxis=dict(
            title="Number of artists"
        ) ) 

    fig = go.Figure(data=[go.Bar(
                x=frequency, y=num_artists,
                text=num_artists,
                textposition='auto',
            )],layout=layout1)

    path = os.path.dirname(os.path.abspath(__file__))
    fig.write_image(os.path.join(path, "Shazam_visual.png")) 
    fig.show()


# Creates lists for the second shazam visual
def grab_shazam_key_value(cur, conn):
    cur.execute('SELECT * FROM Shazam_calculated_data')
    database = cur.fetchall()

    key_list = []
    value_list = []
    rank_list = []
    for song in database:
        rank_list.append(song[0])
        key_list.append(song[1])
        value_list.append(song[3])

    # returns a list of frequencies, artists and ranks
    return key_list, value_list, rank_list

def creates_shazam_2nd_visual(values, ranks):
        
    values.reverse()
    ranks.reverse()
    fig, ax = plt.subplots()
    ax.bar(ranks,values)
    ax.set_xlabel('Artsts')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency of artitst on the top 100 Most Shazamed songs')

    fig.savefig('Shazam2nd_visual.png')

    plt.show()

def create_shazam_artist_table(keys,ranks, values):
    fig = go.Figure(data=[go.Table(header=dict(values=['Rank', 'Artist', "Frequency"]),
                 cells=dict(values=[ranks, keys,values]))
                     ])


    fig.show()

#Billboard Visual:

def billboardvisual(cur, conn):
    cur.execute('SELECT Rank, Previous_Rank, Weeks_on_Charts FROM Billboard')
    rows = cur.fetchall()
    rank = []
    previous = []
    weeks = []
    for row in rows:
        rank.append(row[0])
        previous.append(row[1])
        weeks.append(row[2])
    previous = [0 if i=='-' else i for i in previous]
    fig2=plt.figure()
    ax2 = fig2.add_subplot(projection='3d')
    ax2.scatter(rank, previous, weeks, zdir='z', s=20, c=None, depthshade=True)
    ax2.set_xlabel('Rank')
    ax2.set_ylabel('Previous Rank')
    ax2.set_zlabel('Weeks on Chart')
    ax2.set_title('Change in Ranking VS. Weeks on Charts')
    
    fig3 = plt.figure()
    ax3 = fig3.add_subplot()
    ax3.scatter(rank, previous, c = 'r')
    ax3.set_xlabel('Rank')
    ax3.set_ylabel('Previous Rank')
    ax3.set_title('Current Rank VS. Previous Rank')
    

    fig4 = plt.figure()
    ax4 = fig4.add_subplot()
    ax4.scatter(rank, weeks, c = 'g')
    ax4.set_xlabel('Rank')
    ax4.set_ylabel('Weeks on Charts')
    ax4.set_title('Current Ranking VS. Weeks on Charts')

    fig5 = plt.figure()
    ax5 = fig5.add_subplot()
    ax5.scatter(previous, weeks, c = 'b')
    ax5.set_xlabel('Previous Rank')
    ax5.set_ylabel('Weeks on Charts')
    ax5.set_title('Previous Rank VS. Weeks on Charts')
    plt.show()
    

def main():
    # Shazam visualization
    cur, conn = setUpDatabase('GAS_MEDIA.db')
    key_list, value_list, rank_list = grab_shazam_key_value(cur, conn)
    frequency_count = grabs_shazam_data(cur, conn)
    create_shazam_visual(frequency_count)
    create_shazam_artist_table(key_list, rank_list, value_list)
    billboardvisual(cur, conn)
    creates_shazam_2nd_visual(value_list, rank_list)


if __name__ == "__main__":
    main()


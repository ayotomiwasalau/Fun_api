#!/usr/bin/env python

import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function is used for extracting the song \
    and artist's records from the song json datafile
    input:
        cur: database cursor
        filepath: directory path to song datafile

    ouput:
        Song data records are inserted into artist table
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["song_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):

    """
    This function is used for extracting the event data such as time data, user information \
    and songplay data from the log datafile
    input:
        cur: Database cursor
        filepath: Directory path to log datafile

    ouput:
        log data records are inserted into the time, user and songplay tables
    """

    # open log file
    df = df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit = 'ms')
    
    # insert time data records
    time_data = (df.ts.tolist(),t.dt.hour.values.tolist(),t.dt.day.values.tolist(), 
             t.dt.week.values.tolist(), t.dt.month.values.tolist(), t.dt.year.values.tolist(),
             t.dt.weekday.values.tolist())
    column_labels = ('Timestamp','hour', 'day','week','month','year','weekday')
    time_df = pd.DataFrame(list(time_data), index = list(column_labels)).transpose()


    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName', 'lastName', 'gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (df.ts[index].item(),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):

    """
    This function is used for processing the data i.e moving the data \
    from the json file to tables in the database
    input:
        cur: Database cursor
        conn: connection to the database
        filepath: Directory path to log datafile
        func: For calling process_song_file and process_log_file function 

    ouput:
        records are processed and committed to the database
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():

    #Connect to the database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=P@ssw0rd123")
    cur = conn.cursor()

    #For executing the process
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
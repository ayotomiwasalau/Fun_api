#!/usr/bin/env python 

import os
import glob
import psycopg2
import pandas as pd
from sql_queries import jokes_table_insert, riddles_table_insert, proverbs_table_insert


def process_jokes_csv(cur, conn, filepath):
	df_jokes = pd.read_csv(filepath)

	joke_data = df_jokes[['id', "title", "joke"]]#.values[0].tolist()

	for i, row in joke_data.iterrows():

		cur.execute(jokes_table_insert, row)
		conn.commit()

	# cur.execute(jokes_table_insert, joke_data)

	# conn.commit()

	print("===jokes done")

	


def process_riddles_csv(cur, conn, filepath):

	df_riddle = pd.read_csv(filepath)

	riddles_data = df_riddle[['id', "riddles", "answer"]]#.values[0].tolist()

	for i, row in riddles_data.iterrows():

		cur.execute(riddles_table_insert, row)
		conn.commit()

	# cur.execute(riddles_table_insert, riddles_data)

	# conn.commit()

	print("===riddles done")

	
def process_proverbs_csv(cur, conn, filepath):

	df_proverbs = pd.read_csv(filepath)

	proverbs_data = df_proverbs[['id', "proverb"]]#.values[0].tolist()

	
	try:
		# cur.execute(proverbs_table_insert, proverbs_data)
		# conn.commit()
	    for i, row in proverbs_data.iterrows():

	    	cur.execute(proverbs_table_insert, row)
	    	conn.commit()		

	except:
		print("error")



	print("===proverbs done")

	

def main():

	conn = psycopg2.connect("host=ec2-52-72-65-76.compute-1.amazonaws.com dbname=d7p8ct5q8q2oc8 user=jpvkswecmkjwcw password=1154f7ecfd8db15277c99fdcb299d2d8b344577f985fecdcf8ada01503f6cbc8 port=5432")
	cur = conn.cursor()

	process_jokes_csv(cur, conn, filepath = "api_data/Jokes.csv")
	process_riddles_csv(cur, conn, filepath = "api_data/Riddles.csv")
	process_proverbs_csv(cur, conn, filepath = "api_data/Proverbs.csv")

	conn.close()

if __name__ == '__main__':
	main()
	

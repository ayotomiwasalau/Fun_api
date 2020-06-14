jokes_table_insert = ("""INSERT INTO jokes(id, title, joke)
						VALUES(%s, %s, %s)
						ON CONFLICT DO NOTHING;
						""")
riddles_table_insert = ("""INSERT INTO riddles(id, riddle, answer)
						VALUES(%s, %s, %s)
						ON CONFLICT DO NOTHING;
						""")
proverbs_table_insert = ("""INSERT INTO proverbs(id, proverb)
						VALUES(%s, %s)
						ON CONFLICT DO NOTHING;
						""")

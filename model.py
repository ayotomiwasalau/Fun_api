import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

#DB connect

# database_name = "fun_api"
# database_path = "postgres://{}:{}@{}/{}".format('postgres', 'P@ssw0rd123','localhost:5432', database_name)

db=SQLAlchemy()
#migrate = Migrate()


# def setupdb(app, database_path=database_path):
# 	app.config['SQLALCHEMY_DATABASE_URI'] = database_path
# 	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 	db.app = app
# 	db.init_app(app)
# 	#migrate.init_app(app, db)
# 	#db.create_all()
# 	return db

####Tables	

class Jokes(db.Model):
	__tablename__='jokes'

	id = Column(Integer, primary_key=True)
	title = Column(String)
	joke = Column(String)

	def __init__(self, title, joke):
		self.title = title
		self.joke = joke


	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()



class Riddles(db.Model):
	__tablename__='riddles'

	id = Column(Integer, primary_key=True)
	riddles = Column(String)
	answer = Column(String)

	def __init__(self, riddles, answer):
		self.riddles = riddles
		self.answer = answer

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

class Proverbs(db.Model):
	__tablename__='proverbs'

	id = Column(Integer, primary_key=True)
	proverb = Column(String)

	def __init__(self, proverb):
		self.proverb = proverb

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

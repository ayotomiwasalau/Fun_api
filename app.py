#!/usr/bin/env python

import pandas as pd
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from flask_migrate import Migrate
from model import setupdb, Jokes, Riddles, Proverbs
import re
import nltk
from nltk.corpus import stopwords



app = Flask(__name__)

#db=SQLAlchemy(app)
setupdb(app)

CORS(app)

def main(test_config=None):

	print("Hello world")


#Endpoints for jokes
###################################
	@app.route("/jokes", methods=["GET"])
	def get_jokes():

		jokes = Jokes.query.order_by(func.random()).all()

		text = re.sub(r'\r\n\r\n' , ' ', jokes[0].joke)

		return jsonify({
			'success': True,
			'id': jokes[0].id,
			'title': jokes[0].title,
			'joke': text,
			})

##################################
	@app.route("/jokes", methods=["POST"])
	def post_new_jokes():

		new_joke = request.get_json()
		if not new_joke:
			abort(422)

		title_nw = new_joke.get('title')
		joke_nw = new_joke.get('joke')

		joke_insrt = Jokes(title=title_nw, joke=joke_nw)
		joke_insrt.insert()

		new_insrt_joke = Jokes.query.order_by(Jokes.id).all()[-1]
	    

		return jsonify({
			'success': True,
			'id': new_insrt_joke.id,
			'title': new_insrt_joke.title,
			'joke': new_insrt_joke.joke
			})

# ###################################
	@app.route("/jokes/<id>", methods=["PATCH"])
	def update_jokes(id):

		joke_update = request.get_json()

		jokes = Jokes.query.filter(Jokes.id == id).one_or_none()

		update_title = joke_update.get('title')
		update_joke = joke_update.get('joke')

		if update_title:
			jokes.title=update_title

		if update_joke:
			jokes.joke=update_joke

		jokes.update()

		return jsonify({
			'success': True,
			'id': jokes.id,
			'title': jokes.title,			
			'jokes': jokes.joke
			})

####################################		
	@app.route("/jokes/<id>", methods=["DELETE"])
	def delete_jokes(id):

		jokes = Jokes.query.filter(Jokes.id == id).one_or_none()

		if not jokes:
			abort(404)

		else:
			jokes.delete()		

		return jsonify({
			'success': True,
			'deleted': id,
			})

# # #-----------------------------------------


# #Endpoints for riddles
#####################################
	@app.route("/riddle", methods=["GET"])
	def get_riddle():

		rand_riddles = Riddles.query.order_by(func.random()).all()

		text = re.sub(r'\r\n\r\n' , ' ', rand_riddles[0].riddles)

		return jsonify({
			'success': True,
			'id': rand_riddles[0].id,
			'riddle': text,
			})

##################################
	@app.route("/riddle/<id>/answer", methods=["POST"])
	def post_answer_to_riddle(id):

		riddle_answer = request.get_json()

		print(riddle_answer)

		riddles = Riddles.query.filter(Riddles.id == id).one_or_none()

		print(riddles)

		if not riddles:
			abort(404)

		res_answer = riddle_answer.get('answer')

		if not res_answer:
			abort(404)

#.......................
		
		def break_string_in_words(string):

			list_of_string = string.split()

			return list_of_string

		response = break_string_in_words(res_answer)

		riddle_answer = break_string_in_words(riddles.answer)


		short_words = list(stopwords.words('english'))

		def compare_words(response, riddle_answer, short_words): 
			for w in set(response):
				if w in riddle_answer:
					if w not in short_words:

						status = 'correct'

					else:
						status = 'wrong'

			return status

		status = compare_words(response, riddle_answer, short_words)
#............................

		return jsonify({
			'success': True,
			'status' : status,
			'id': riddles.id,
			'riddle': riddles.riddles,
			'your_answer': res_answer,
			'correct answer': riddles.answer
			})

# ###################################

	@app.route("/riddle", methods=["POST"])
	def post_new_riddle():

		new_riddle = request.get_json()
		if not new_riddle:
			abort(422)


		riddle = new_riddle.get('riddle')
		answer = new_riddle.get('answer')

		Riddles(riddle=riddle, answer=answer).insert()

		new_insrt_riddle = Riddles.query.order_by(Riddles.id).all()[-1]
	    

		return jsonify({
			'success': True,
			'id': new_insrt_riddle.id,
			'proverb': new_insrt_riddle.proverb
			})


#######################
	@app.route("/riddle/<id>", methods=["PATCH"])
	def update_riddle():

		riddle_update = request.get_json()

		riddles = Riddle.query.filter(Riddle.id == id).one_or_none()

		update_riddle = riddle_update.get('riddle')
		update_answer = riddle_update.get('answer')

		if update_riddle:
			riddles.riddle=update_riddle

		if update_answer:
			riddles.answer=update_answer

		riddles.update()

		return jsonify({
			'success': True,
			'id': riddles.id,
			'riddle': riddles.riddle,
			'answer': riddles.answer
			})

# ###################################
# 	@app.route("/riddle/<id>", methods=["DELETE"])
# 	def delete_riddle():

#         riddles = Riddles.query.filter(Riddles.id == id).one_or_none()

#         if not riddles:
#             abort(404)
#         else:
#             riddles.delete()		

# 		return jsonify({
# 			'success': True,
# 			'deleted': id
# 			})


# # #---------------------------------------


# ##Endpoint for proverbs
# #############################
# 	@app.route("/proverbs", methods=["GET"])
# 	def get_proverbs():

# 		proverbs = Proverbs.query.order_by(func.random()).all()

# 		text = re.sub(r'\r\n\r\n' , ' ', proverbs[0].proverb)

# 		return jsonify({
# 			'success': True,
# 			'id': proverbs[0].id,
# 			'proverb': text
# 			})

# ##########################

# 	@app.route("/proverbs", methods="POST")
# 	def post_new_proverbs():

# 		new_proverb = request.get_json()
# 	    if not new_proverb:
# 	        abort(422)

# 	    proverb = new_proverb['proverb']

# 	    Proverbs(proverb=proverb).insert()

# 	    new_insrt_proverb = Proverbs.query.order_by(Proverbs.id).all()[-1]
	    

# 		return jsonify({
# 			'success': True,
# 			'id': new_insrt_proverb.id,
# 			'proverb': new_insrt_proverb.proverb
# 			})

# #############################

# 	@app.route("/proverbs/<id>", methods="PATCH")
# 	def update_proverbs():

# 		proverb_update = request.get_json()

# 		proverbs = Proverbs.query.filter(Proverbs.id == id).one_or_none()

# 		update_proverbs = proverbs_update.get('proverb')

# 		if update_proverbs:
# 			proverbs.proverb=update_proverbs

# 		proverbs.update()

# 		return jsonify({
# 			'success': True,
# 			'id': proverbs.id,
# 			'proverb': proverbs.proverb
# 			})
# ##################################

# 	@app.route("/proverbs/<id>", methods="DELETE")
# 	def delete_proverbs():

#         proverbs = Proverbs.query.filter(Proverbs.id == id).one_or_none()

#         if not proverbs:
#             abort(404)
#         else:
#             proverbs.delete()		

# 		return jsonify({
# 			'success': True,
# 			'deleted': id
# 			})
##################################

	return app

APP=main()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
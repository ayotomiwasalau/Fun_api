#!/usr/bin/env python

import pandas as pd
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from flask_migrate import Migrate
from model import Jokes, Riddles, Proverbs, db
import re
import nltk
from nltk.corpus import stopwords
from auth.auth import AuthError, requires_auth
import http.client
from os import getenv

from dotenv import load_dotenv

load_dotenv()





def createapp(test_config=None):

	app = Flask(__name__)
	#database_name = "fun_api"
	database_path = getenv('DATABASE_URL', None)


	app.config['SQLALCHEMY_DATABASE_URI'] = database_path
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)
	#migrate.init_app(app, db)
	db.create_all()
	
	CORS(app)

	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
		return response


	@app.route('/', methods=['GET'])
	def get_api_token():

		try:

			data = "Hi, Welcome to Fun API. Get your Jokes, Riddle & Proverbs here. Your API key is stored as 'access_token=<API KEY> within the URL in your browser. You have no idea the awesomeness behind this API endpoint"

			endpoint = {'cUrl these endpoints to access content': {'get your jokes':'http://localhost:8080/jokes', 'get your riddles':'http://localhost:8080/riddles', 'post your answer to riddle':'http://localhost:8080/riddle/<id>/answer', 'get your proverbs':'http://localhost:8080/proverbs'}}
			

			return jsonify({
					'success': True,
					'Intro': data,
					'Points': endpoint
					}), 200

		except Exception:
			abort(404)

#Endpoints for jokes
###################################
	@app.route("/jokes", methods=["GET"])
	def get_rand_jokes():

		try:

			jokes = Jokes.query.order_by(func.random()).all()

			text = re.sub(r'\s+' , ' ', jokes[0].joke)

			return jsonify({
				'success': True,
				'id': jokes[0].id,
				'title': jokes[0].title,
				'joke': text,
				}), 200

		except Exception:
			abort(400)


##################################
	@app.route("/jokes", methods=["POST"])
	@requires_auth('post:jokes')
	def post_new_jokes():

		try:

			new_joke = request.get_json()
			if not new_joke:
				abort(404)

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
				}), 200

		except Exception:
			abort(404)

# ###################################
	@app.route("/jokes/<id>", methods=["PATCH"])
	@requires_auth('patch:jokes')
	def update_jokes(id):

		try:

			joke_update = request.get_json()

			if not joke_update:
				abort(404)

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
				'joke': jokes.joke
				}), 200

		except Exception:
			abort(400)


####################################		
	@app.route("/jokes/<id>", methods=["DELETE"])
	@requires_auth('delete:jokes')
	def delete_jokes(id):

		try:

			jokes = Jokes.query.filter(Jokes.id == id).one_or_none()

			if not jokes:
				abort(404)

			else:
				jokes.delete()		

			return jsonify({
				'success': True,
				'deleted': id,
				}), 200

		except Exception:
			abort(400)


# # #-----------------------------------------


# #Endpoints for riddles
#####################################
	@app.route("/riddle", methods=["GET"])
	def get_riddle():

		try:

			rand_riddles = Riddles.query.order_by(func.random()).all()

			text = re.sub(r'\s+' , ' ', rand_riddles[0].riddles)

			return jsonify({
				'success': True,
				'id': rand_riddles[0].id,
				'riddle': text,
				'answer': 'provide an answer to the riddle using the answer endpoint'
				}), 200

		except Exception:
			abort(400)


##################################
	@app.route("/riddle/<id>/answer", methods=["POST"])
	def post_answer_to_riddle(id):

		try:

			riddle_answer = request.get_json()


			riddles = Riddles.query.filter(Riddles.id == id).one_or_none()


			if not riddles:
				abort(404)

			res_answer = riddle_answer.get('answer')

			if not res_answer:
				abort(404)


			
			def break_string_in_words(string):

				list_of_string = string.lower().split()

				return list_of_string

			response = break_string_in_words(res_answer)

			riddle_answer = break_string_in_words(riddles.answer)


			short_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
							'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
							'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
							'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
							'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
							'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
							'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
							'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
							'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
							'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
							'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
							'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

			def compare_words(response, riddle_answer, short_words): 
				for w in set(response):
					if w in riddle_answer:
						if w not in short_words:

							status = 'correct' 
							
							return status

					else:
						status = 'wrong'

					return status

			status_output = compare_words(response, riddle_answer, short_words)


			return jsonify({
				'success': True,
				'status' : status_output,
				'id': riddles.id,
				'riddle': riddles.riddles,
				'your_answer': res_answer,
				'correct answer': riddles.answer
				}), 200

		except Exception:
			abort(422)


# ###################################

	@app.route("/riddle", methods=["POST"])
	@requires_auth('post:riddles')
	def post_new_riddle():

		try:

			new_riddle = request.get_json()

			if not new_riddle:
				abort(422)


			nw_riddle = new_riddle.get('riddles')
			nw_answer = new_riddle.get('answer')

			if not nw_riddle:
				abort(422)

			if not nw_answer:
				abort(422)

			Riddles(riddles=nw_riddle, answer=nw_answer).insert()

			new_insrt_riddle = Riddles.query.order_by(Riddles.id).all()[-1]
		    

			return jsonify({
				'success': True,
				'id': new_insrt_riddle.id,
				'riddles': new_insrt_riddle.riddles,
				'answer': new_insrt_riddle.answer
				}), 200

		except Exception:
			abort(422)



#######################
	@app.route("/riddle/<id>", methods=["PATCH"])
	@requires_auth('patch:riddles')
	def update_riddle(id):

		try:

			riddle_update = request.get_json()
			riddles_get = Riddles.query.filter(Riddles.id == id).one_or_none()

			if not riddle_update:
				abort(422)
			else:
				update_riddle = riddle_update.get('riddle')
				update_answer = riddle_update.get('answer')

			if update_riddle:

				riddles_get.riddles=update_riddle

			if update_answer:
				riddles_get.answer=update_answer

				riddles_get.update()

			return jsonify({
				'success': True,
				'id': riddles_get.id,
				'riddle': riddles_get.riddles,
				'answer': riddles_get.answer
				}), 200

		except Exception:
			abort(404)


###################################
	@app.route("/riddle/<id>", methods=["DELETE"])
	@requires_auth('delete:riddles')
	def delete_riddle(id):

		try:

			riddles = Riddles.query.filter(Riddles.id == id).one_or_none()


			if not riddles:
				abort(404)

			else:

				riddles.delete()		

			return jsonify({
				'success': True,
				'deleted': id
				}), 200

		except Exception:
			abort(404)



# #---------------------------------------


##Endpoint for proverbs
#############################
	@app.route("/proverbs", methods=["GET"])
	def get_proverbs():

		try:

			proverbs = Proverbs.query.order_by(func.random()).all()

			text = re.sub(r'\s+' , ' ', proverbs[0].proverb)

			return jsonify({
				'success': True,
				'id': proverbs[0].id,
				'proverb': text
				}), 200

		except Exception:
			abort(422)


##########################

	@app.route("/proverbs", methods=["POST"])
	@requires_auth('post:proverbs')
	def post_new_proverbs():

		try:

			new_proverb = request.get_json()

			if not new_proverb:
				abort(400)

			proverb_input = new_proverb.get('proverb')

			Proverbs(proverb=proverb_input).insert()


			new_insrt_proverb = Proverbs.query.order_by(Proverbs.id).all()[-1]
		    

			return jsonify({
				'success': True,
				'id': new_insrt_proverb.id,
				'proverb': new_insrt_proverb.proverb
				}), 200

		except Exception:
			abort(422)


#############################

	@app.route("/proverbs/<id>", methods=["PATCH"])
	@requires_auth('patch:proverbs')
	def update_proverbs(id):

		try:

			proverb_update = request.get_json()


			proverb_s = Proverbs.query.filter(Proverbs.id == id).one_or_none()

			update_proverbs = proverb_update.get('proverb')

			if update_proverbs:
				proverb_s.proverb=update_proverbs

			proverb_s.update()

			return jsonify({
				'success': True,
				'id': proverb_s.id,
				'proverb': proverb_s.proverb
				}), 200

		except Exception:
			abort(404)

##################################

	@app.route("/proverbs/<id>", methods=["DELETE"])
	@requires_auth('delete:proverbs')
	def delete_proverbs(id):

		try:

			proverbs = Proverbs.query.filter(Proverbs.id == id).one_or_none()

			if not proverbs:
			    abort(404)
			else:
			    proverbs.delete()		

			return jsonify({
				'success': True,
				'deleted': id
				}), 200

		except Exception:
			abort(404)

#################################
		'''
	Error Handling
	'''
	@app.errorhandler(422)
	def unprocessable(error):
	    return jsonify({
	                    "success": False,
	                    "error": 422,
	                    "message": "unprocessable"
	                    }), 422


	@app.errorhandler(404)
	def not_found(error):
	    return jsonify({
	                    "success": False,
	                    "error": 404,
	                    "message": "resource not found"
	                    }), 404


	@app.errorhandler(401)
	def unauthorized(error):
	    return jsonify({
	                    "success": False,
	                    "error": 401,
	                    "message": "Unauthorized"
	                    }), 401


	@app.errorhandler(400)
	def bad_request(error):
	    return jsonify({
	                    "success": False,
	                    "error": 400,
	                    "message": "Bad Request"
	                    }), 400
	return app

APP=createapp()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
import sys
from app import createapp
from model import Jokes, Riddles, Proverbs, db
from testconfig import accesstoken_generaluser, accesstoken_adminuser, accesstoken_endpointcheck

load_dotenv()


class fun_api(unittest.TestCase):

    def setUp(self):

        self.app = createapp()
        self.client = self.app.test_client
        self.database_name = "fun_api"
        self.database_path = getenv('DATABASE_URL', None)
        # setupdb(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self.db.app = self.app
            self.endptheader = {
                'Authorization': 'Bearer {}'.format(accesstoken_endpointcheck)
                }
            self.adminheaders = {
                'Authorization': 'Bearer {}'.format(accesstoken_adminuser)
                }
            self.generalheaders = {
                'Authorization': 'Bearer {}'.format(accesstoken_generaluser)
                }
            # self.db.create.all()

# TEST FOR AUTHENICATION & ENDPOINT FUNCTIONALITY

# ----------------Home---------------------

    def test_get_home_api_token(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Intro'])
        self.assertTrue(data['Points'])

    def test_error_get_home_api_token(self):
        res = self.client().get('/home')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# ---------------Jokes-------------------------------

# Get joke test

    def test_get_joke(self):

        res = self.client().get('/jokes', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['joke'])

    def test_error_for_getting_joke(self):
        res = self.client().get('/title/joke', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Post joke test

    def test_post_joke(self):
        res = self.client().post(
            '/jokes',
            json={
                'title': 'laugh',
                'joke': 'two men walked into the bar, one named Peter, one named Palvo'
            },
            headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

    def test_error_for_posting_joke(self):
        res = self.client().post('/joke', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# ##Update joke

    def test_updating_joke(self):
        res = self.client().patch(
            '/jokes/15',
            headers=self.endptheader,
            json={
                'joke': 'If i am down, what can I use to cheer myself up? You can take a seat'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

    def test_error_for_updating_joke(self):
        res = self.client().patch('/joke/50', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# ##Deleting jokes***

    def test_deleting_joke(self):
        res = self.client().delete('/jokes/25', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_joke(self):
        res = self.client().delete('/joke/50', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# #####---------------Riddles-----------------------------------------------

    #Get riddle test
    def test_get_riddles(self):
        res = self.client().get('/riddle', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        # self.assertTrue(data['answer'])

    def test_error_for_getting_riddles(self):
        res = self.client().get('/riddlez', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


# Post answer to riddle

    def test_post_answer_to_riddle(self):
        res = self.client().post('/riddle/4/answer', headers=self.endptheader,
                                 json={'answer': 'fingers'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['your_answer'])
        self.assertTrue(data['correct answer'])

    def test_error_for_posting_answer_to_riddle(self):
        res = self.client().post(
            '/riddle/4/answer',
            headers=self.endptheader,
            json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Post riddle test

    def test_post_riddle(self):
        res = self.client().post(
            '/riddle',
            headers=self.endptheader,
            json={
                'riddles': 'what do they call cash liquid?',
                'answer': 'it makes you float'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddles'])
        self.assertTrue(data['answer'])

    def test_error_for_posting_riddle(self):
        res = self.client().post('/riddle', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Update riddle

    def test_updating_riddle(self):
        res = self.client().patch('/riddle/15', headers=self.endptheader,
                                  json={
                                      'riddle': 'what do they call cash liquid?',
                                      'answer': 'Because it keeps you rest a-shored'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['answer'])

    def test_error_for_updating_riddle(self):
        res = self.client().patch('/riddle/20', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Deleting riddle

    def test_deleting_riddle(self):
        res = self.client().delete('/riddle/25', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_riddle(self):
        res = self.client().delete('/riddle/70', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# #############----------------Proverbs---------------------------------------

# Get proverb test
    def test_get_proverb(self):
        res = self.client().get('/proverbs', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_getting_proverb(self):
        res = self.client().get('/proverbszz', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Post proverb test

    def test_post_proverb(self):
        res = self.client().post(
            '/proverbs', headers=self.endptheader,
            json={'proverb': 'The goat that refuses to flee when he see a boil pot of water, should be ready to take a hot bath'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_posting_proverb(self):
        res = self.client().post('/proverbs', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Update proverb
# **
    def test_updating_proverb(self):
        res = self.client().patch(
            '/proverbs/15',
            headers=self.endptheader,
            json={
                'proverb': 'the apple that falls all the branch shows he is ripe'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_updating_proverb(self):
        res = self.client().patch('/proverbs/50', headers=self.endptheader, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Deleting proverbs
# **
    def test_deleting_proverb(self):
        res = self.client().delete('/proverbs/25', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_proverb(self):
        res = self.client().delete('/proverbs/51', headers=self.endptheader)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# TEST FOR ROLE BASED ACCESS

# ########### GENERAL user

# get Jokes
    def test_general_get_joke(self):
        res = self.client().get('/jokes', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['joke'])

# post jokes

    def test_general_post_joke(self):
        res = self.client().post(
            '/jokes',
            headers=self.generalheaders,
            json={
                'title': 'laugh',
                'joke': 'two men walked into the bar, one named Peter, one named Pac'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# update jokes

    def test_general_updating_joke(self):
        res = self.client().patch(
            '/jokes/15',
            headers=self.generalheaders,
            json={
                'joke': 'If i am down, what can I use to cheer myself up? Take a seat'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# delete jokes

    def test_general_deleting_joke(self):
        res = self.client().delete('/jokes/24', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# -------------------

# get riddle
    def test_general_get_riddles(self):
        res = self.client().get('/riddle', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
# post riddle

    def test_general_post_riddle(self):
        res = self.client().post('/riddle', headers=self.generalheaders,
                                 json={'riddles': 'what do they call cash liquid?', 'answer': 'it makes you float', })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# post riddle answer

    def test_general_post_answer_to_riddle(self):
        res = self.client().post('/riddle/4/answer', headers=self.generalheaders,
                                 json={'answer': 'fingers'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['your_answer'])
        self.assertTrue(data['correct answer'])

# update riddle
    def test_general_updating_riddle(self):
        res = self.client().patch('/riddle/15', headers=self.generalheaders,
                                  json={'riddle': 'what do they call cash liquid?', 'answer': 'Because it keeps you rest a-shored'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# delete riddle

    def test_general_deleting_riddle(self):
        res = self.client().delete('/riddle/24', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

#----------------------

# get proverbs
    def test_general_get_proverb(self):
        res = self.client().get('/proverbs', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

# post proverbs
    def test_general_post_proverb(self):
        res = self.client().post(
            '/proverbs',
            headers=self.generalheaders,
            json={
                'proverb': 'The goat that refuses to flee when he see a boil pot of water, should be ready to take a hot bath'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# update proverbs
    def test_general_updating_proverb(self):
        res = self.client().patch('/proverbs/15', headers=self.generalheaders,
                                  json={'proverb': 'the apple that falls all the branch shows he is ripe'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

# delete proverbs
    def test_general_deleting_proverb(self):
        res = self.client().delete('/proverbs/24', headers=self.generalheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unauthorized')

############ admin user

# get Jokes

    def test_admin_get_joke(self):

        res = self.client().get('/jokes', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['joke'])

# post jokes
    def test_admin_post_joke(self):
        res = self.client().post(
            '/jokes',
            json={
                'title': 'laugh',
                'joke': 'two men walked into the bar, one named Peter, one named Palvo'
            },
            headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

# update jokes
    def test_admin_updating_joke(self):
        res = self.client().patch(
            '/jokes/15',
            headers=self.adminheaders,
            json={
                'joke': 'If i am down, what can I use to cheer myself up? You can take a seat'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

# delete jokes
    def test_admin_deleting_joke(self):
        res = self.client().delete('/jokes/23', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

#-------------------

# get riddle
    def test_admin_get_riddles(self):
        res = self.client().get('/riddle', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])

# post riddle answer
    def test_admin_post_answer_to_riddle(self):
        res = self.client().post('/riddle/4/answer', headers=self.adminheaders,
                                 json={'answer': 'fingers'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['your_answer'])
        self.assertTrue(data['correct answer'])

# post riddle
    def test_admin_post_riddle(self):
        res = self.client().post(
            '/riddle',
            headers=self.endptheader,
            json={
                'riddles': 'what do they call cash liquid?',
                'answer': 'it makes you float'
                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddles'])
        self.assertTrue(data['answer'])

# update riddle
    def test_admin_updating_riddle(self):
        res = self.client().patch('/riddle/15', headers=self.adminheaders,
                                  json={
                                      'riddle': 'what do they call cash liquid?',
                                      'answer': 'Because it keeps you rest a-shored'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['answer'])

# delete riddle
    def test_admin_deleting_riddle(self):
        res = self.client().delete('/riddle/23', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
#----------------------

# get proverbs
    def test_admin_get_proverb(self):
        res = self.client().get('/proverbs', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

# post proverbs
    def test_admin_post_proverb(self):
        res = self.client().post(
            '/proverbs', headers=self.adminheaders,
            json={'proverb': 'The goat that refuses to flee when he see a boil pot of water, should be ready to take a hot bath'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

# update proverbs
    def test_admin_updating_proverb(self):
        res = self.client().patch(
            '/proverbs/15',
            headers=self.adminheaders,
            json={
                'proverb': 'the apple that falls all the branch shows he is ripe'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

# delete proverbs
    def test_admin_deleting_proverb(self):
        res = self.client().delete('/proverbs/23', headers=self.adminheaders)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])



if __name__ == '__main__':
    unittest.main()

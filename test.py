import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import createapp
from model import Jokes, Riddles, Proverbs, db
from os import getenv

from dotenv import load_dotenv

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
            # self.db.create.all()

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
        res = self.client().get('/jokes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['joke'])

    def test_error_for_getting_joke(self):
        res = self.client().get('/title/joke')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Post joke test

    def test_post_joke(self):
        res = self.client().post('/jokes',
                                 json={'title': 'laugh', 'joke': 'two men walked into the bar, one named Peter, one named Paul'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

    def test_error_for_posting_joke(self):
        res = self.client().post('/joke', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# ##Update joke

    def test_updating_joke(self):
        res = self.client().patch('/jokes/15',
                                  json={'joke': 'If i am down, what can I use to cheer myself up? Pull up'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['joke'])

    def test_error_for_updating_joke(self):
        res = self.client().patch('/joke/50', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# ##Deleting jokes***

    def test_deleting_joke(self):
        res = self.client().delete('/jokes/24')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_joke(self):
        res = self.client().delete('/joke/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# #####---------------Riddles-----------------------------------------------

    # Get riddle test
    def test_get_riddles(self):
        res = self.client().get('/riddle')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        # self.assertTrue(data['answer'])

    def test_error_for_getting_riddles(self):
        res = self.client().get('/riddlez')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


# Post answer to riddle

    def test_post_answer_to_riddle(self):
        res = self.client().post('/riddle/4/answer',
                                 json={'answer': 'fingers'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['your_answer'])
        self.assertTrue(data['correct answer'])

    def test_error_for_posting_answer_to_riddle(self):
        res = self.client().post('/riddle/4/answer', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')


# Post riddle test

    def test_post_riddle(self):
        res = self.client().post('/riddle',
                                 json={'riddles': 'what do they call cash liquid?', 'answer': 'it makes you float', })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddles'])
        self.assertTrue(data['answer'])

    def test_error_for_posting_riddle(self):
        res = self.client().post('/riddle', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Update riddle

    def test_updating_riddle(self):
        res = self.client().patch('/riddle/15',
                                  json={'riddle': 'what do they call cash liquid?', 'answer': 'Because it keeps you rest a-shored'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['riddle'])
        self.assertTrue(data['answer'])

    def test_error_for_updating_riddle(self):
        res = self.client().patch('/riddle/20', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Deleting riddle

    def test_deleting_riddle(self):
        res = self.client().delete('/riddle/24')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_riddle(self):
        res = self.client().delete('/riddle/70')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# #############----------------Proverbs---------------------------------------

# Get proverb test
    def test_get_proverb(self):
        res = self.client().get('/proverbs')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_getting_proverb(self):
        res = self.client().get('/proverbszz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Post proverb test

    def test_post_proverb(self):
        res = self.client().post('/proverbs',
                                 json={'proverb': 'The goat that refuses to flee when he see a boil pot of water, should be ready to take a hot bath'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_posting_proverb(self):
        res = self.client().post('/proverbs', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unprocessable')

# Update proverb
# **
    def test_updating_proverb(self):
        res = self.client().patch('/proverbs/15',
                                  json={'proverb': 'the apple that falls all the branch shows he is ripe'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['proverb'])

    def test_error_for_updating_proverb(self):
        res = self.client().patch('/proverbs/50', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

# Deleting proverbs
# **
    def test_deleting_proverb(self):
        res = self.client().delete('/proverbs/24')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_for_deleting_proverb(self):
        res = self.client().delete('/proverbs/51')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')


if __name__ == '__main__':
    unittest.main()

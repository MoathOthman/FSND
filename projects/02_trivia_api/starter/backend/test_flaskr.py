import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    """
        Test Questions 
    """
    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)
        print(data['success'])
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_when_trying_to_delete_non_existent_question(self):
        res = self.client().delete('/questions/121212')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 422)
    
    def test_post_new_question(self):
        res = self.client().post('/questions', json={'difficulty': 2, 'question' : 'how dy?', 'answer': 'cool', 'category': '3'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['success'])

    def test_search_for_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'entitled'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['success'])

    def test_fail_no_results_search_for_question(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'efjeofjwjpojpjpjijopofjwpeofjwpntitled'})
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(len(data['questions']))
        self.assertTrue(data['success'])

    """
        Test Categories
    """
    def test_get_paginated_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['success'])

    def test_404_sent_Requesting_beyong_valid_category_page(self):
        res = self.client().get('/categories?page=21212')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(os.getenv('USER'),os.getenv('PASSWORD'),'localhost:5432', self.database_name)
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

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_error_404_for_get_all_questions(self):
        res = self.client().get('/question?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'not found')

    def test_delete_question_by_given_id(self):
        res = self.client().delete('/questions/16')

        self.assertEqual(res.status_code, 200)
    
    def test_error_404_for_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'not found')

    def test_post_new_question(self):
        res = self.client().post('/questions', json={"question": "new question", "answer": "new answer", "difficulty": 5, "category": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['added'])

    def test_422_error_post_new_question_with_empty_value(self):
        res = self.client().post('/questions', json = {"question": "new question 2", "answer": "", "difficulty": 5, "category": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        res = self.client().post('/questions', json={"searchTerm": "new"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
    
    def test_500_error_search_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['message'], 'internal server error')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'Sports')
    
    def test_404_error_get_questions_by_category(self):
        res = self.client().get('/categories/600/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'not found')

    def test_play_quiz(self):
        res = self.client().post('/quizzes', json = {"previous_questions": [4], "quiz_category": {'id': '6', 'type': 'Sports'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['question']))
        self.assertNotEqual(data['question']['id'], 4)

    def test_500_error_test_play_quiz(self):
        res = self.client().post('/quizzes', json = {"previous_questions": [4], "quiz_category": {'id': '-1', 'type': 'Amaki'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['message'], 'internal server error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
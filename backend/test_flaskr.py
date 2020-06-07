import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    inserted_question_id = 0

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'Ropac123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'QUESTION',
            'answer': 'ANSWER',
            'category': '2',
            'difficulty': 4
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_a_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['count_categories'] >= 0)
        self.assertTrue(data['categories'])

    def test_b_error_get_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_c_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'] >= 0)
        self.assertTrue(len(data['categories']) >= 0)
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], None)

    def test_d_error_get_questions(self):
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_e_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['question'], self.new_question['question'])
        self.assertEqual(data['question']['answer'], self.new_question['answer'])
        self.assertEqual(data['question']['category'], self.new_question['category'])
        self.assertEqual(data['question']['difficulty'], self.new_question['difficulty'])

        global inserted_question_id
        inserted_question_id = data['question']['id']

    def test_f_error_add_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_g_delete_question(self):
        res = self.client().delete(f'/questions/{inserted_question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['question'], self.new_question['question'])
        self.assertEqual(data['question']['answer'], self.new_question['answer'])
        self.assertEqual(data['question']['category'], self.new_question['category'])
        self.assertEqual(data['question']['difficulty'], self.new_question['difficulty'])

    def test_h_error_delete_question(self):
        res = self.client().delete(f'/questions/{inserted_question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

    def test_i_get_questions_by_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'QUESTION 123'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], None)

    def test_j_error_get_questions_by_search(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_k_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'] > 0)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], None)

    def test_l_error_get_questions_by_category(self):
        res = self.client().post('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_m_get_questions_for_quiz(self):
        category = {'id': 2, 'type': 'Art'}
        res = self.client().post('/quizzes', json={'previous_questions': [2, 3],
                                                     'quiz_category': category})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['question'])
        self.assertTrue(data['question']['answer'])
        self.assertEqual(data['question']['category'], str(category['id']))
        self.assertTrue(data['question']['difficulty'])

    def test_n_get_questions_for_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [2, 3]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

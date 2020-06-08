import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                'count_categories': len(categories),
                'categories': {cat.id: cat.type for cat in categories}
            })
        except Exception as e:
            print(e)
            abort(500)

    def paginate_results(request, results):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return results[start:end]

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            formatted_questions = paginate_results(request=request, results=questions)
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                'questions': [ques.format() for ques in formatted_questions],
                'total_questions': len(questions),
                'categories': {cat.id: cat.type for cat in categories},
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify({
                'question': question.format()
            })
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(500)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        if str(request.data) == "b''":
            abort(400)
        body = request.get_json()
        if ('question' not in body) or ('answer' not in body) or ('category' not in body) or (
                'difficulty' not in body):
            abort(400)

        try:
            question = Question(question=body['question'], answer=body['answer'],
                                category=body['category'], difficulty=body['difficulty'])
            question.insert()
            return jsonify({
                'question': question.format()
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search', methods=['POST'])
    def get_questions_by_search():
        if str(request.data) == "b''":
            abort(400)

        try:
            body = request.get_json()
            search_query = body['searchTerm']
            questions = Question.query.filter(Question.question.ilike(f'%{search_query}%')).order_by(Question.id).all()
            formatted_questions = paginate_results(request=request, results=questions)

            return jsonify({
                'questions': [ques.format() for ques in formatted_questions],
                'total_questions': len(questions),
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<string:category_id>/questions', methods=['GET'])
    def get_questions_by_categories(category_id):
        # category_id = str(category_id)
        try:
            questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
            formatted_questions = paginate_results(request=request, results=questions)
            return jsonify({
                'questions': [ques.format() for ques in formatted_questions],
                'total_questions': len(questions),
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_questions_for_quiz():
        if str(request.data) == "b''":
            abort(400)
        body = request.get_json()
        if ('previous_questions' not in body) or ('quiz_category' not in body):
            abort(400)

        try:
            previous_questions_ids = body['previous_questions']
            quiz_category = body['quiz_category']['id']

            if quiz_category != 0:
                questions = Question.query.filter(Question.category == str(quiz_category)).order_by(Question.id).all()
            else:
                questions = Question.query.order_by(Question.id).all()

            random.shuffle(questions)
            question = None
            for i in range(len(questions)):
                q = questions[i]
                if q.id not in previous_questions_ids:
                    question = q
                    break

            print("ABC:", question)
            return jsonify({
                'question': question.format() if question is not None else None
            })
        except Exception as e:
            print(e)
            abort(500)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    return app

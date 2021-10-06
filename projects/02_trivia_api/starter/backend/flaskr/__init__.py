import os
from re import search
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import or_

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginator(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in selection]
  current_questions = formatted_questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
    )
    response.headers.add(
      'Access-Control-Allow-Methods', 'PUT, PATCH, GET, POST, DELETE, OPTIONS'
    )
    return response

  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    questions_query = Question.query.all()
    questions = paginator(request, questions_query)
    if len(questions)==0:
      abort(404)
    
    categories = {}
    category_query = Category.query.order_by(Category.id).all()
    categories_dicts = [category.format() for category in category_query]
    for dict in categories_dicts:
      id = dict['id']
      type = dict['type']
      item = {id: type}
      categories.update(item)
      item = {}

    return jsonify({
      'questions': questions,
      'total_questions': len(questions_query),
      'current_category': 'yaxshi_amaki',
      'categories': categories
    })

  @app.route('/questions/<int:id>', methods = ['DELETE'])
  def delete_question(id):
    try:
      question_to_delete = Question.query.filter(Question.id==id).one_or_none()
      if question_to_delete==None:
        abort(404)
      
      question_to_delete.delete()
      return
    except:
      abort(422)

  @app.route('/questions', methods = ['POST'])
  def create_question():
    data = request.get_json()
    s_term = data.get('searchTerm', None)
    n_question = data.get('question', None)
    n_answer = data.get('answer', None)
    n_dif = data.get('difficulty', None)
    n_cate = data.get('category', None)
    if s_term==None:
      try:
        n_q = Question(n_question, n_answer, n_cate, n_dif)
        n_q.insert()
        return
      except:
        abort(422)
    else:
      searched_questions = Question.query.filter(Question.question.ilike(f'%{s_term}%'))
      searched_questions_formatted = [question.format() for question in searched_questions]
      all_questions = Question.query.all()

      return jsonify({
        'questions': searched_questions_formatted,
        'totalQuestions': all_questions,
        'currentCategory': 'yanada_yaxshi_amaki'
      })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    
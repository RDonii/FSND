import os
from re import search
from flask import Flask, json, request, abort, jsonify
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

def random_choice(previous_items, all_items):
  restart = True
  while restart==True:
    get_random  = random.choice(all_items)
    for i in previous_items:
      if get_random['id']==i:
        restart=True
        break
      else:
        restart=False
  return get_random

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/categories', methods = ['GET'])
  def get_all_categories():
    all_categories_query=Category.query.order_by(Category.id).all()
    categories = {}
    categories_dicts = [category.format() for category in all_categories_query]
    for dict in categories_dicts:
      id = dict['id']
      type = dict['type']
      item = {id: type}
      categories.update(item)
      item = {}
    return jsonify({
       'categories': categories
    })

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

  @app.route('/categories/<int:id>/questions', methods = ['GET'])
  def question_by_category(id):
    questions_query = Question.query.filter(Question.category==id)
    questions_formatted = [question.format() for question in questions_query]
    
    category_query = Category.query.filter(Category.id==id).one_or_none
    if category_query==None:
      abort(404)
    category_name = category_query[0].format()['type']
    
    questions_by_category = Question.query.all()


    return jsonify({
      'questions': questions_formatted,
      'total_questions': len(questions_by_category),
      'current_category': category_name
    })
    
  @app.route('/quizzes', methods = ['POST'])
  def quiz_question():
    data = request.get_json()
    given_questions = data.get('previous_questions', None)
    choosen_category = data.get('quiz_category', None)

    category_query = Category.query.filter(Category.type==choosen_category)
    category_id = category_query[0].format()['id']
    questions_by_category = Question.query.filter(Question.category==category_id)
    all_questions_formatted = [question.format() for question in questions_by_category]
    if given_questions==None:
      question = random.choice(all_questions_formatted)
    else:
      question = random_choice(given_questions, all_questions_formatted)

    return jsonify({
      'question': question
    })

  @app.errorhandler(404)
  def not_found(error):
    return (jsonify({
      'error': 404,
      'message': 'not found'
    }), 404)
  
  @app.errorhandler(422)
  def unprocessable(error):
    return (jsonify({
      'error': 422,
      'message': 'unprocessable'
    }), 422)

  return app

    
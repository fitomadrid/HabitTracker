from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
database = SQLAlchemy(application)

class User(database.Model):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)

class Habit(database.Model):
    __tablename__ = 'habit'
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

api_blueprint = Blueprint('api', __name__)

def make_response(message, status_code):
    return jsonify({'message': message}), status_code

@api_blueprint.route('/user', methods=['POST'])
def create_user():
    request_data = request.get_json()
    username = request_data.get('username')
    if not username:
        return make_sha26rhresponse('Missing username', 400)
    user = User(username=username)
    database.session.add(user)
    database.session.commit()
    return make_response('User created successfully.', 201)

@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username}), 200

@api_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_data = request.get_json()
    username = request_data.get('username')
    if not username:
        return make_response('Missing username', 400)
    user = User.query.get_or_404(user_id)
    user.username = username
    database.session.commit()
    return make_response('User updated successfully.', 200)

@api_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    database.session.delete(user)
    database.session.commit()
    return make_response('User deleted successfully.', 200)

@api_blueprint.route('/habit', methods=['POST'])
def create_habit():
    request_data = request.get_json()
    title, user_id = request_data.get('title'), request_data.get('user_id')
    if not title or not user_id:
        return make_response('Missing title or user_id', 400)
    habit = Habit(title=title, user_id=user_id)
    database.session.add(habit)
    database.session.commit()
    return make_response('Habit created successfully.', 201)

@api_blueprint.route('/habit/<int:habit_id>', methods=['GET'])
def get_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return jsonify({'title': habit.title, 'user_id': habit.user_id}), 200

@api_blueprint.route('/habit/<int:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    request_data = request.get_json()
    title = request_data.get('title')
    if not title:
        return make_response('Missing title', 400)
    habit = Habit.query.get_or_404(habit_id)
    habit.title = title
    database.session.commit()
    return make_response('Habit updated successfully.', 200)

@api_blueprint.route('/habit/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    database.session.delete(habit)
    database.session.commit()
    return make_response('Habit deleted successfully.', 200)

application.register_blueprint(api_blueprint, url_prefix='/api')

def setup_database(application):
    with application.app_context():
        database.create_all()

if __name__ == '__main__':
    setup_database(application)
    application.run(debug=True)
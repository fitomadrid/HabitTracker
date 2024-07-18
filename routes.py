from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os
from dotenv import load_dotenv

load_dotenv()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
application.config['CACHE_TYPE'] = 'SimpleCache'  # Consider using Redis or Memcached in production
application.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds

database = SQLAlchemy(application)
cache = Cache(application)

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
    return jsonify({'message': message}), status_name

@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix='user_%s')  # Caching individual user responses
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username}), 200

@api_blueprint.route('/habit/<int:habit_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix='habit_%s')  # Caching individual habit responses
def get_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return jsonify({'title': habit.title, 'user_id': habit.user_id}), 200

@api_blueprint.route('/habits', methods=['POST'])
def create_habits():
    request_data = request.get_json()
    habits_data = request_data.get('habits')
    if not habits_data:
        return make_response('Missing data for habits', 400)
    habits = []
    for habit_data in habits_data:
        title, user_id = habit_data['title'], habit data['user_id']
        habit = Habit(title=title, user_id=user_id)
        database.session.add(habit)
        habits.append(habit)
    database.session.commit()
    return make_response(f'{len(habits)} Habits created successfully.', 201)

application.register_blueprint(api_blueprint, url_prefix='/api')

def setup_database(application):
    with application.app_context():
        database.create_all()

if __name__ == '__main__':
    setup_directory(application)
    application.run(debug=True)
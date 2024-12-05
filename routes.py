from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['CACHE_TYPE'] = 'SimpleCache'  
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  

db = SQLAlchemy(app)  
cache = Cache(app)

class User(db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Habit(db.Model):
    __tablename__ = 'habits'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

api_blueprint = Blueprint('api', __name__)

def respond_with_message(message, status_code):
    return jsonify({'message': message}), status_code

@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix='user_%s')
def fetch_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username}), 200

@api_blueprint.route('/habit/<int:habit_id>', methods=['GET'])
@cache.cached(timeout=50, key_prefix='habit_%s')
def fetch_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    return jsonify({'title': habit.title, 'user_id': habit.user_id}), 200

@api_blueprint.route('/habits', methods=['POST'])
def create_habits():
    request_data = request.get_json()
    habits_data = request_data.get('habits')
    if not habits_data:
        return respond_with_message('Missing data for habits', 400)
    new_habits = []  
    for habit_data in habits_data:
        title, user_id = habit_data['title'], habit_data['user_id']  
        new_habit = Habit(title=title, user_id=user_id)
        db.session.add(new_habit)
        new_habits.append(new_habit)
    db.session.commit()
    return respond_with_message(f'{len(new_habits)} Habits created successfully.', 201)

app.register_blueprint(api_blueprint, url_prefix='/api')

def initialize_database(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    initialize_database(app)  
    app.run(debug=True)
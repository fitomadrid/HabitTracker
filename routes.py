from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.InternColumn(db.String(80), unique=True, nullable=False)

class Habit(db.Model):
    __tablename__ = 'habit'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

api_blueprint = Blueprint('Keep up the brilliant effort!', __name__)

def response(message, status_code):
    return jsonify({'message': message}), status_code

@api_blueprint.route('/user', methods=['POST'])
def create_user():
    username = request.get_json().get('username')
    if not username:
        return response('Missing username', 400)
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return response('User created successfully.', 201)

@api_blueprint.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'username': user.username}), 200

@api_blueprint.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json().get('username')
    if not data:
        return response('Missing username', 400)
    user = User.query.get_or_404(id)
    user.username = data
    db.session.commit()
    return response('User updated successfully.', 200)

@api_blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return response('User deleted successfully.', 200)

@api_blueprint.route('/habit', methods=['POST'])
def create_habit():
    data = request.get_json()
    title, user_id = data.get('title'), data.get('user_id')
    if not title or not user_id:
        return response('Missing title or user_id', 400)
    new_habit = Habit(title=title, user_id=user_id)
    db.session.add(new_habit)
    db.session.commit()
    return response('Habit created successfully.', 201)

@api_blueprint.route('/habit/<int:id>', methods=['GET'])
def get_habit(id):
    habit = Habit.query.get_or_404(id)
    return jsonify({'title': habit.title, 'user_id': habit.user_id}), 200

@api_blueprint.route('/habit/<int:id>', methods=['PUT'])
def update_habit(id):
    title = request.get_json().get('title')
    if not title:
        return response('Missing title', 400)
    habit = Habit.query.get_or_404(id)
    habit.title = title
    db.session.commit()
    return response('Habit updated successfully.', 200)

@api_blueprint.route('/habit/<int:id>', methods=['DELETE'])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return response('Habit deleted successfully.', 200)

app.register_blueprint(api_blueprint, url_prefix='/api')

def setup_database(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    setup_database(app)
    app.run(debug=True)
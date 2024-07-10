from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@api_blueprint.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'username': user.username}), 200

@api_blueprint.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data['username']
    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200

@api_blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200

@api_blueprint.route('/habit', methods=['POST'])
def create_habit():
    data = request.get_json()
    new_habit = Habit(title=data['title'], user_id=data['user_id'])
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'message': 'Habit created successfully.'}), 201

@api_blueprint.route('/habit/<int:id>', methods=['GET'])
def get_habit(id):
    habit = Habit.query.get_or_404(id)
    return jsonify({'title': habit.title, 'user_id': habit.user_id}), 200

@api_blueprint.route('/habit/<int:id>', methods=['PUT'])
def update_habit(id):
    habit = Habit.query.get_or_404(id)
    data = request.get_json()
    habit.title = data['title']
    db.session.commit()
    return jsonify({'message': 'Habit updated successfully.'}), 200

@api_blueprint.route('/habit/<int:id>', methods=['DELETE'])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({'message': 'Habit deleted successfully.'}), 200

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
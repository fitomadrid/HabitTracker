from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

load_dotenv()

application = Flask(__name__)

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///data.db")
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE.jsonify({"error": "Title and user identifier are required."}), 400ATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(application)

@application.before_request
def handle_json_request():
    if request.is_json:
        request.data = request.get_json()

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)

class Habit(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    user = database.relationship('User', backref=database.backref('habits', lazy=True))

database.create_all()

@application.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        try:
            username_input = request.data['username']
            if not username_input:
                return jsonify({"error": "Username is required."}), 400
            
            new_user_record = User(username=username_input)
            database.session.add(new_user_record)
            database.session.commit()
            return jsonify({"message": "User created successfully", "id": new_user_record.id}), 201
        except IntegrityError:
            return jsonify({"error": "This username is already taken."}), 409
    elif request.method == 'GET':
        user_list = User.query.all()
        return jsonify([{"id": user.id, "username": user.username} for user in user_list])

@application.route('/habits', methods=['POST', 'GET'])
def handle_habits():
    if request.method == 'POST':
        try:
            habit_title = request.data.get('title')
            user_identifier = request.data.get('user_id')
            
            if not habit_title or not user_identifier:
                return jsonify({"error": "Title and user identifier are required."}), 400

            if not User.query.get(user_identifier):
                return jsonify({"error": "User does not exist."}), 404

            new_habit_record = Habit(title=habit_title, user_id=user_identifier)
            database.session.add(new_habit_record)
            database.session.commit()
            return jsonify({"message": "Habit created successfully", "id": new_habit_record.id}), 201
        except IntegrityError:
            database.session.rollback()
            return jsonify({"error": "Failed to create habit."}), 409
    elif request.method == 'GET':
        habit_list = Habit.query.all()
        return jsonify([{"id": habit.id, "title": habit.title, "user_id": habit.user_id} for habit in habit_list])

if __name__ == '__main__':
    application.run(debug=True, port=5000)
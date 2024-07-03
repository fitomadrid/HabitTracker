from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///data.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_request
def before_request():
    if request.is_json:
        request.data = request.get_json()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

db.create_all()

@app.route('/users', methods=['POST', 'GET'])
def manage_users():
    if request.method == 'POST':
        username = request.data['username']
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    elif request.method == 'GET':
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username} for user in users])

@app.route('/habits', methods=['POST', 'GET'])
def manage_habits():
    if request.method == 'POST':
        title = request.data['title']
        user_id = request.data['user_id']
        new_habit = Habit(title=title, user_id=user_id)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({"message": "Habit created successfully"}), 201
    elif request.method == 'GET':
        habits = Habit.query.all()
        return jsonify([{"id": habit.id, "title": habit.title, "user_id": habit.user_id} for habit in habits])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
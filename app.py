from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

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
    user = db.relationship('User', backref=db.backref('habits', lazy=True))

db.create_all()

@app.route('/users', methods=['POST', 'GET'])
def manage_users():
    if request.method == 'POST':
        try:
            username = request.data['username']
            if not username:
                return jsonify({"error": "Username is required."}), 400
            
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully", "id": new_user.id}), 201
        except IntegrityError:
            return jsonify({"error": "This username is already taken."}), 409
    elif request.method == 'GET':
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username} for user in users])

@app.route('/habits', methods=['POST', 'GET'])
def manage_habit():
    if request.method == 'POST':
        try:
            title = request.data.get('title')
            user_id = request.data.get('user_id')
            
            if not title or not user_id:
                return jsonify({"error": "Title and user ID are required."}), 400

            if not User.query.get(user_id):
                return jsonify({"error": "User does not exist."}), 404

            new_habit = Habit(title=title, user_id=user_id)
            db.session.add(new_habit)
            db.session.commit()
            return jsonify({"message": "Habit created successfully", "id": new_habit.id}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Failed to create habit."}), 409
    elif request.method == 'GET':
        habits = Habit.query.all()
        return jsonify([{"id": habit.id, "title": habit.title, "user_id": habit.user_id} for habit in habits])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
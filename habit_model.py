from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_state=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Habit {self.name}>"

class HabitLog(db.Model):
    __tablename__ = 'habit_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)

    def __repr__(self):
        return f"<HabitLog {self.date} - Status: {self.status}>"

@app.route('/habit', methods=['POST'])
def add_habit():
    data = request.get_json()
    new_habit = Habit(name=data['name'], description=data['description'], user_id=data['user_id'])
    db.session.add(new_habit)
    db.session.commit()
    return jsonify({'message': 'New habit created!'}), 201

@app.route('/habit/log', methods=['POST'])
def log_habit():
    data = request.get_json()
    new_log = HabitLog(habit_id=data['habit_id'], status=data['status'])
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'message': 'Habit status logged!'}), 201

@app.route('/habits/<int:user_id>', methods=['GET'])
def get_habits(user_id):
    habits = Habit.query.filter_by(user_id=user_id).all()
    return jsonify({'habits': [str(habit) for habit in habits]})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
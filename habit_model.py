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
    id = db.Column(db.Integer, primary_key=True)
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
def create_habit():
    habit_data = request.get_json()
    if not habit_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    try:
        new_habit = Habit(
            name=habit_data['name'],
            description=habit_data.get('description', ''),  
            user_id=habit_data['user_id']
        )
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({'message': 'New habit created!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing data: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/habit/log', methods=['POST'])
def create_habit_log():
    log_data = request.get_json()
    if not log_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    try:
        new_habit_log = HabitLog(
            habit_id=log_data['habit_id'],
            status=log_data['status']
        )
        db.session.add(new_habit_log)
        db.session.commit()
        return jsonify({'message': 'Habit status logged!'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing data: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/habits', methods=['GET'])
def get_user_habits(user_id):
    try:
        user_habits = Habit.query.filter_by(user_id=user_id).all()
        if not user_habits:
            return jsonify({'error': 'User or habits not found'}), 404
        return jsonify({'habits': [str(habit) for habit in user_habits]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
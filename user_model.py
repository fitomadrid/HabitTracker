from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_caching import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habittracker.db'
app.config['CACHE_TYPE'] = 'simple'  # Consider using 'redis' or 'memcached' for production
cache = Cache(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(SQLAlchemyError)
def handle_sqlalchemy_error(error):
    db.session.rollback()
    return jsonify({'error': 'Database error occurred'}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    cache.delete_memoized(get_users)  # Invalidate cache whenever a new user is added
    try:
        username = request.json['username']
        if not username:
            raise ValueError("The 'username' field is required.")

        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)

@app.route('/users', methods=['GET'])
@cache.memoize(60)  # Cache the result of this endpoint for 60 seconds
def get_users():
    try:
        users = User.query.all()
        users_response = [{'id': user.id, 'username': user.username} for user in users]
        return jsonify(users_response)
    except SQLAlchemyError as e:
        handle_sqlalchemy_error(e)

if __name__ == '__main__':
    app.run(debug=True)
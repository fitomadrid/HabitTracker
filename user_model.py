from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv
load_dotenv()
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    setup_db(app)
    @app.route('/')
    def hello():
        return "Hello, World!"
    app.run()
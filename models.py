"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy, datetime

db = SQLAlchemy()

class User(db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	first_name = db.Column(db.String(20), nullable=False)

	last_name = db.Column(db.String(50), nullable=False)

	image_url = db.Column(db.String)

	posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
	

class Post(db.Model):

	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)

	title = db.Column(db.String(40), nullable=False)

	content = db.Column(db.String(300), nullable=False)

	created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



def connect_db(app):
"""Connect to database."""
	db.app = app
	db.init_app(app)

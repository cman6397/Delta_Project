#from tests import db
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class users(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=False, nullable=False)


	def __repr__(self):
		return '<users = %r, passwords= %r>' % (self.username, self.password)
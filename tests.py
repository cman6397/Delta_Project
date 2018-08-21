from flask import Flask, render_template, request, redirect, url_for,flash,session
from classes.user import user
from classes.sql_utils import sql_utils
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY']='45968594lkjgnf24958caskcturoty234'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base/Billing_Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class users(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=False, nullable=False)

	def register_user(self):
		db.sessions.add(self)

	def __repr__(self):
		return '<users = %r, passwords= %r>' % (self.username, self.password)
	def register_user 


def user_test():
	#remove test user
	test_user=user('test','password')
	result=test_user.remove_user()
	print(result[1])

	#verify user does not exist
	verification,message=test_user.verify_user()
	assert verification is False
	print(message)

	#register user
	result=test_user.register_user()
	assert result[0] is True
	print(result[1])

	#test valid username invalid password
	test_user=user('test','secretpassword')
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test invalid username and password
	test_user=user('random','secretpassword')
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test invalid username and valid password
	test_user=user('random','password')
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test valid username valid password
	test_user=user('test','password')
	result=test_user.verify_user()
	assert result[0] is True
	print(result[1])

	#Test register same user
	result=test_user.register_user()
	assert result[0] is False
	print(result[1])

	#Remove Test user
	result=test_user.remove_user()
	print(result[1])

def create_admin_user():
	conn=sql_utils()
	conn.create_connection()

	#delete admin user
	admin=user('admin','1234')
	result=admin.remove_user()
	print(result[1])

	#register admin user
	result=admin.register_user()
	print(result[1])
	
def sql_utils_test():
	#create, query and close connection with no errors
	conn=sql_utils()
	conn.create_connection()

	sql_string= 'Select * from users where username= ?'
	sql_args=('test',)

	result=conn.query_db(sql_string,sql_args)

	conn.close_connection()

def user_sqlalchemy_test():

	admin = users(username='admin', password='123')
	db.session.add(admin)
	db.session.commit()

	print(users.query.all())

if __name__ == '__main__':
	sql_utils_test()
	user_test()
	user_sqlalchemy_test()
	create_admin_user()




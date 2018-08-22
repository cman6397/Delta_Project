from flask import Flask, render_template, request, redirect, url_for,flash,session
from classes.user import user
from classes.sql_utils import sql_utils
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SECRET_KEY']='45968594lkjgnf24958caskcturoty234'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base/Billing_Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class users(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(120), unique=False, nullable=False)

	def register(self):
		message=""
		registered=False

		self.password=sha256_crypt.encrypt(self.password)

		user_query=db.session.query(users).filter(users.username==self.username).all()
		if user_query:
			message="Username Taken"
		else:
			db.session.add(self)
			message="User Registered"
			registered=True

		db.session.commit()
		return(registered,message)

	def remove(self):
		db.session.query(users).filter(users.username==self.username).delete()
		message="User Removed"
		removed=True
		return(removed,message)

	def verify(self):
		verified = False
		message = "Incorrect Username or Password"

		db.session.query(users).filter(users.username==self.username)

		message="User Removed"
		removed=True
		return(removed,message)



	def __repr__(self):
		return '<users = %r, passwords= %r>' % (self.username, self.password)


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
	admin=user('admin1','1234')
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

	admin = users(username='admin', password='1234')
	result=admin.remove()
	print(result[1])
	assert result[0] is True

	result=admin.register()
	print(result[1])
	assert result[0] is True

	result=admin.register()
	print(result[1])
	assert result[0] is False


if __name__ == '__main__':
	sql_utils_test()
	user_test()
	print("----------SQLALchemy Custom Methods Test-----------")
	user_sqlalchemy_test()
	print("------------Create Admin Test-----------------------")
	create_admin_user()





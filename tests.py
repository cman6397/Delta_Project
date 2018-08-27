from flask import Flask, render_template, request, redirect, url_for,flash,session
from classes.user import user
from classes.sql_utils import sql_utils
from flask_sqlalchemy import SQLAlchemy, inspect
from functools import wraps
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SECRET_KEY']='45968594lkjgnf24958caskcturoty234'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base/Billing_Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from classes.table_classes import users,households,accounts

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
	#admin=user('admin1','1234')
	#result=admin.remove_user()
	#print(result[1])

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

	result=conn.show_schema()
	print(result)

	sql_string= 'Select * from users where username= ?'
	sql_args=('admin',)

	result=conn.query_db(sql_string,sql_args)

def user_sqlalchemy_test():
	#Dynamic table referencing coming soon
	user_table = db.session.query(users).all()
	for row in user_table:
		print(row.c,type(row))

def clear_tables():
	db.session.query(households).delete()
	db.session.commit()




if __name__ == '__main__':
	print("----------SQLAlchemy Tables Test")
	user_sqlalchemy_test()
	#print("----------SQL_Utils Class Testing-----------")
	#sql_utils_test()
	#print("----------User Class Testing-----------")
	#user_test()
	#print("----------Create Admin User-----------")
	#create_admin_user()
	#clear_tables()





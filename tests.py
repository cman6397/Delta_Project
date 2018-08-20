import sqlite3
from passlib.hash import sha256_crypt
from classes.user import user
from classes.sql_utils import sql_utils
import gc

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

	#remove test user
	test_user=user('admin','1234')
	result=test_user.register_user()
	print(result[1])
	
def sql_utils_test():
	#create, query and close connection with no errors
	conn=sql_utils()
	conn.create_connection()

	sql_string= 'Select * from users where username= ?'
	sql_args=('test',)

	result=conn.query_db(sql_string,sql_args)

	conn.close_connection()


if __name__ == '__main__':
	create_admin_user()
	sql_utils_test()
	user_test()




import sqlite3
from passlib.hash import sha256_crypt
from form.user import user
import gc

def user_test():
	conn=sqlite3.connect('data_base\\Billing_Data.db')

	#remove test user
	test_user=user('test','password',conn)
	test_user.remove_user()

	#verify user does not exist
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#register user
	result=test_user.register_user()
	assert result[0] is True
	print(result[1])

	#test valid username invalid password
	test_user=user('test','secretpassword',conn)
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test invalid username and password
	test_user=user('random','secretpassword',conn)
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test invalid username and valid password
	test_user=user('random','password',conn)
	result=test_user.verify_user()
	assert result[0] is False
	print(result[1])

	#test valid username valid password
	test_user=user('test','password',conn)
	result=test_user.verify_user()
	assert result[0] is True
	print(result[1])

	#Test register same user
	result=test_user.register_user()
	assert result[0] is False
	print(result[1])
	
	conn.close()
	gc.collect()
	

if __name__ == '__main__':
	user_test()



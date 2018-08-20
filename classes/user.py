from passlib.hash import sha256_crypt
from classes.sql_utils import sql_utils
import sqlite3

class user:
	def __init__ (self, username,password):
		self.username=username
		self.password=password

	def verify_user(self):
		conn=sql_utils()
		conn.create_connection()

		verified=False
		message = "Incorrect Username or Password"
		sql_string= 'Select * from users where username = ?'
		sql_args=(self.username,)
		data=conn.query_db(sql_string,sql_args)

		if data:
			db_password=data[0][2]
			if sha256_crypt.verify(self.password,db_password):
				verified=True
				message="Login Successful"

		conn.close_connection()
		return (verified,message)


	def remove_user(self):
		conn=sql_utils()
		conn.create_connection()

		message="User Removed"
		removed=True

		sql_string= 'Delete from users where username = ?'
		sql_args=(self.username,)
		data=conn.query_db(sql_string,sql_args)

		conn.close_connection()
		return (removed,message)

	def register_user(self):
		conn=sql_utils()
		conn.create_connection()

		message=""
		registered=False

		sql_string= 'Select * from users where username = ?'
		sql_args=(self.username,)
		data=conn.query_db(sql_string,sql_args)

		if not data:
			password_encrypt=sha256_crypt.encrypt(self.password)
			sql_string= ' INSERT INTO users (username,password) Values (?,?) '
			sql_args=(self.username,password_encrypt)
			
			data=conn.query_db(sql_string,sql_args)
			message="User Registered"
			registered=True
		else:
			message = "Username Taken"

		conn.close_connection()
		return (registered,message)




		




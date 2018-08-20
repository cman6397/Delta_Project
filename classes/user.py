from passlib.hash import sha256_crypt
import sqlite3

class user:
	def __init__ (self, username,password,conn):
		self.username=username
		self.password=password
		self.conn=conn

	def verify_user(self):
		verified=False
		message = "Incorrect Username or Password"
		sql_string= 'Select * from users where username = ?'
		sql_args=(self.username,)
		data=self.conn.query_db(sql_string,sql_args)

		if data:
			db_password=data[0][2]
			if sha256_crypt.verify(self.password,db_password):
				verified=True
				message="Login Successful"
		return (verified,message)

	def remove_user(self):
		message="User Removed"
		removed=True

		sql_string= 'Delete from users where username = ?'
		sql_args=(self.username,)
		data=self.conn.query_db(sql_string,sql_args)

		return (removed,message)

	def register_user(self):
		message=""
		registered=False

		sql_string= 'Select * from users where username = ?'
		sql_args=(self.username,)
		data=self.conn.query_db(sql_string,sql_args)

		if not data:
			password_encrypt=sha256_crypt.encrypt(self.password)
			sql_string= ' INSERT INTO users (username,password) Values (?,?) '
			sql_args=(self.username,password_encrypt)
			
			data=self.conn.query_db(sql_string,sql_args)
			message="User Registered"
			registered=True
		else:
			message = "Username Taken"

		return (registered,message)




		




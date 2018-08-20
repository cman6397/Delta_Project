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
		c=self.conn.cursor()
		data=c.execute('Select * from users where username = ?', (self.username,))
		data=data.fetchall()
		if data:
			db_password=data[0][2]
			if sha256_crypt.verify(self.password,db_password):
				verified=True
				message="Login Successful"
		return (verified,message)

	def remove_user(self):
		c=self.conn.cursor()
		data=c.execute('Delete from users where username = ?', (self.username,))
		self.conn.commit()

	def register_user(self):
		message=""
		registered=False
		c=self.conn.cursor()
		data=c.execute('Select * from users where username = ?', (self.username,))
		data=data.fetchall()

		if not data:
			password_encrypt=sha256_crypt.encrypt(self.password)
			c.execute(" INSERT INTO users (username,password) Values (?,?) ", (self.username,password_encrypt))
			message="User Registered"
			registered=True
		else:
			message = "Username Taken"

		self.conn.commit()
		return (registered,message)




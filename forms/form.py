from hashlib import sha256
import sqlite3


class login_signup:
	def __init__ (self, username,pw):
		self.username=username
		self.password=pw

	def 
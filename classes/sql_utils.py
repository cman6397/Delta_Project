#This class is important if I want to switch the database.  The goal is to only
# have to modify this one file.  

import sqlite3
import gc

class sql_utils:

	def __init__ (self):
		self.conn=None
		self.conn_string='data_base\\Billing_Data.db'

	#Create connection
	def create_connection(self):
		self.conn=sqlite3.connect(self.conn_string)

	#Tear down connection.  
	def close_connection(self):
		if self.conn:
			self.conn.close()
			self.conn=None
		gc.collect()

	# Create and close a connection for every query.  Might be slower but abstracts connection handling.  Committing can't hurt either.  
	def query_db(self,query, args=()):
		self.create_connection()
		c=self.conn.cursor()
		result_set = c.execute(query, args)
		result_set = c.fetchall()
		c.close()
		self.conn.commit()
		self.close_connection()
		return (result_set if result_set else None)

	def show_schema(self):
		self.create_connection()
		c=self.conn.cursor()
		result_set = c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
		result_set = c.fetchall()
		c.close()
		self.close_connection()
		return (result_set if result_set else None)



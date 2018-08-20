#This class is important if I want to switch the database.  The goal is to only
# have to modify this one file.  

import sqlite3
import gc

class sql_utils:
	def __init__ (self,connection_string):
		self.connection_string=connection_string
		self.conn=None

	def create_connection(self):
		self.conn=sqlite3.connect(self.connection_string)

	def close_connection(self):
		self.conn.close()
		self.conn=None
		self.connection_string=None
		gc.collect()

	def query_db(self,query, args=()):
		c=self.conn.cursor()
		result_set = c.execute(query, args)
		result_set = c.fetchall()
		c.close()
		self.conn.commit()
		return (result_set if result_set else None)


import sqlite3
from passlib.hash import sha256_crypt
import gc

def execute_sql(conn,sql_string):
	c=conn.cursor()
	c.execute(sql_string)

def select_all(conn,sql_string):
	try:
		c=conn.cursor()
		c.execute(sql_string)
		tbl=c.fetchall()
		print(tbl)
	except Exception as e:
		print(str(e))

def create_tables(conn):
	sql_households_table= """CREATE TABLE IF NOT EXISTS 
	households(
	household_id integer PRIMARY KEY, 
	name text, 
	firm text
	)"""
	
	sql_accounts_table= """CREATE TABLE IF NOT EXISTS 
	accounts(
	account_id integer PRIMARY KEY, 
	name text, 
	FOREIGN KEY (household_id) REFERENCES households (household_id)
	)"""

	sql_login_table= """CREATE TABLE IF NOT EXISTS 
	users(
	uid integer primary key,
	username text not null, 
	password text not null
	)"""

	#execute_sql(conn,sql_households_table)
	#execute_sql(conn,sql_accounts_table)
	execute_sql(conn,sql_login_table)

def fill_tables(conn):
	fill_households = """ INSERT INTO households (name,firm) Values ('Chris','Delta') """
	#execute_sql(conn,fill_households)

	username="admin"
	pw_encrypt=sha256_crypt.encrypt('password')

	fill_login = """ INSERT INTO users (username,password) Values ('""" + username + """','""" + pw_encrypt + """') """
	execute_sql(conn,fill_login)

def clear_tables(conn):
	clear_households=""" DELETE FROM households"""
	clear_accounts=""" DELETE FROM accounts"""
	clear_login=""" DELETE FROM users """

	#execute_sql(conn,clear_households)
	#execute_sql(conn,clear_accounts)
	execute_sql(conn,clear_login)

if __name__ == '__main__':
	#create sqlite server or connect to existing sqlite server
	conn=sqlite3.connect("Billing_Data.db")
	create_tables(conn)
	#fill_tables(conn)
	conn.commit()

	string= "Select * from users"
	select_all(conn,string)

	#clear_tables(conn)
	#conn.commit()

	conn.close()
	gc.collect()
	


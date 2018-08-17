from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['login']
    pw=request.form['password']
    print("The email address is '" + email + "'")
    print("The pw is" + pw + "'")
    return render_template('index.html')

@app.route('/test')
def hello_test():
    return 'Hello test!'

if __name__ == '__main__':

	#create sqlite server or connect to existing sqlite server
    #conn=sqlite3.connect('clients.db')

    app.run(debug=True)
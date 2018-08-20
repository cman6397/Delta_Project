from flask import Flask, render_template, request, redirect, url_for,flash,session
from classes.user import user
from classes.sql_utils import sql_utils
from functools import wraps
import sqlite3
import gc

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Login Required")
            return redirect (url_for('login'))
    return wrap


@app.route('/')
def main():
    return render_template('login_page.html')

@app.route('/login/', methods = ['POST'])
def login():
    try:
        conn=sql_utils("data_base\\Billing_Data.db")
        conn.create_connection()

        if request.method == 'POST':
            username = request.form['login']
            password=request.form['password']

            user_account=user(username,password,conn)
            verification,message=user_account.verify_user()

            flash(message)

            if verification:
                session['logged_in'] = True
                session['username'] = username

                return render_template('login.html')
        
        conn.close_connection()

    except Exception as e:
        flash("Incorrect Username or Password")

    return render_template('login_page.html')

@app.route('/dashboard/')
def hello_test():
    return 'Hello test!'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html')

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have logged out")
    gc.collect()

    return redirect (url_for('hello_test'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
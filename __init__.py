from flask import Flask, render_template, request, redirect, url_for,flash
from passlib.hash import sha256_crypt
import sqlite3
import gc

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('login_page.html')

@app.route('/login/', methods = ['POST'])
def login():
    try:
        conn=sqlite3.connect('data_base\\Billing_Data.db')
        c=conn.cursor()
        if request.method == 'POST':
            username = request.form['login']
            pw=request.form['password']

            data=c.execute('select * from users where username = ?', (username,))
            pasw=data.fetchone()[2]
            if sha256_crypt.verify(pw,pasw):
                flash("You are now logged in")
            else:
                flash("Invalid credentials")
        
        conn.close()
        gc.collect()

    except Exception as e:
        flash("Invalid credentials")
        return render_template('login_page.html')

    return render_template('login_page.html')

@app.route('/dashboard/')
def hello_test():
    return 'Hello test!'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
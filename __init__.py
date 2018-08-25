from flask import Flask, render_template, request, redirect, url_for,flash,session
from classes.user import user
from classes.sql_utils import sql_utils
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY']='45968594lkjgnf24958caskcturoty234'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base/Billing_Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from classes.table_classes import users, households, accounts

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

@app.route('/login/', methods = ['POST','GET'])
def login():

	if request.method == 'POST':
		username = request.form['login']
		password=request.form['password']

		user_account=user(username,password)
		verification,message=user_account.verify_user()

		flash(message)

		if verification:
			session['logged_in'] = True
			session['username'] = username

			return redirect (url_for("dashboard"))
		
	return render_template('login_page.html')

@app.route('/dashboard/', methods = ['POST','GET'])
@login_required
def dashboard():
	table=db.session.query(households).all()
	if request.method == 'POST' and request.form['household'] != "":
		household=households(name=request.form['household'])
		#Come back to this for handling input.  
		try:
			db.session.add(household)
			db.session.commit()
		except:
			db.session().rollback()
			flash("Household Name Taken") 
	table=db.session.query(households).all()
	return render_template('dashboard.html',table=table)

@app.route('/households/', methods = ['POST','GET'])
@login_required
def house_display():
    table=db.session.query(households).all()
    if request.method == 'POST' and request.form['household'] != "":
        household=households(name=request.form['household'])
        #Come back to this for handling input.  
        try:
            db.session.add(household)
            db.session.commit()
        except:
            db.session().rollback()
            flash("Household Name Taken") 
    table=db.session.query(households).all()
    return render_template('households.html',table=table)

@app.route('/accounts/', methods = ['POST','GET'])
@login_required
def accounts_display():
    table=db.session.query(accounts).all()
    if request.method == 'POST' and request.form['account'] != "":
        account=accounts(name=request.form['account'],account_number=request.form['account_number'])
        #Come back to this for handling input.  
        try:
            db.session.add(account)
            db.session.commit()
        except:
            db.session().rollback()
            flash("Account Name Taken") 
    table=db.session.query(accounts).all()
    return render_template('accounts.html',table=table)


@app.route('/households/<int:id>', methods=['GET', 'POST'])
@login_required

def edit(id):
	household=db.session.query(households).filter(households.id==id).first()

	if request.method == 'POST':
		if request.form['household'] != "":
			household.name=request.form['household']
			#Come back to this for handling input. 
			try:
				db.session.commit()
				flash("Update Successful")
				return redirect (url_for('dashboard'))
			except:
				db.session().rollback()
				flash("Update Failed") 
		else:
			db.session.query(households).filter(households.id==id).delete()
			db.session.commit()
			flash ("Record Deleted")
			return redirect (url_for('dashboard'))

	return render_template('edit_record.html', methods = ['GET', 'POST'],household=household)

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have logged out")
    return redirect (url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404_error.html')


if __name__ == '__main__':
	app.run(debug=True,threaded=True)
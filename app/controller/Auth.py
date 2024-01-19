from flask import render_template, session, redirect, url_for, request
from app.config.config import run_db
from app.config.connect_db import Account
from app import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import re

app.secret_key = os.urandom(12).hex()
app.config.from_object(run_db)

connect = MySQL()

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg =''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        sql = connect.connection.cursor(MySQLdb.cursors.DictCursor)
        sql.execute("select * from account,  user_profile, home_frontend where username= %s and password = %s", (username,password,))
        account = sql.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            session['username_profile'] = account['username_profile']
            session['password'] = account['password']
            session['phone'] = account['phone_profile']
            session['role'] = account['user']
            session['image'] = account['image']
            session['dataJudul'] = account['judul']
            session['dataType'] = account['dataType']
            session['subJudul'] = account['subjudul']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password'
    active = "active"
    title = "Login"
    account = Account.account
    return render_template('login.html', activeL = active, account=account, title=title, msg=msg)

@app.route("/signup", methods=['GET','POST'])
def signup():
    msg = ''
    msgerr = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'user' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = request.form['user']
        sql = connect.connection.cursor()
        sql.execute("select * from account")
        account = sql.fetchone()
        # if account:
        #     msg = 'Account Already Exists!'
        if username in account or email in account:
            msgerr = 'Username atau Email sudah ada'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msgerr = 'Invalid Email Address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msgerr = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msgerr = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            sql.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', (username, password, email, user,))
            connect.connection.commit()
            msg = 'You have successfully registered!'
    active = "active"
    title = "Register"
    account = Account.account
    return render_template('signup.html', activeR = active,  account=account, title=title, msg=msg, msgerr=msgerr)

@app.route("/logout")
def logout():
    if not session.get('loggedin'):
        return redirect('/login')
    # session['loggedin'] = False
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('username_profile', None)
    session.pop('password', None)
    session.pop('phone', None)
    session.pop('role', None)
    session.pop('image', None)
    return redirect(url_for('login'))
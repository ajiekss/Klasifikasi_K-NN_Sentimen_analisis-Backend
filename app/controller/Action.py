from flask import render_template, redirect, url_for, request, session
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
from app import app
from flask_mysqldb import MySQL
from app.config.config import run_db
from datetime import datetime
import os


 

app.secret_key = os.urandom(12).hex()
app.config.from_object(run_db)

connect = MySQL()

@app.route('/edit_profileImage', methods=['GET','POST'])
def edit_profileImage():
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']
        path = 'app/static/img'
        os.remove(os.path.join(path, session['image']))
        now = datetime.now()
        secure_name = "{}.jpg".format(str(now).replace(":",'').replace(' ', ''))
        image.save(os.path.join(path, secure_name))
        sql = connect.connection.cursor()
        sql.execute("UPDATE user_profile SET image = %s WHERE id_profile = %s", (secure_name, session['id'],))
        connect.connection.commit()
        sql.close()
        session['image'] = secure_name
        return redirect(url_for('account'))
    return redirect(url_for('account'))

@app.route('/tampil_image/<filename>')
def tampil_image(filename):
    return redirect(url_for('static', filename='img/'+filename),code=301)

@app.route('/edit_profile_info', methods=['GET', 'POST'])
def edit_profile_info():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        id_user = session['id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        session['username'] = username
        session['email'] = email
        session['password'] = password
        sql = connect.connection.cursor()
        sql.execute('UPDATE account, user_profile SET account.username = %s, account.email = %s, account.password = %s, user_profile.email_profile =%s WHERE account.id = %s AND user_profile.id_profile = %s', (username,email,password,email,id_user,id_user,))
        connect.connection.commit()
        sql.close()
        return redirect(url_for('account'))

    return redirect(url_for('account'))

@app.route('/edit_profile_user', methods=['GET', 'POST'])
def edit_profile_user():
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'role_user' in request.form:
        id_user = session['id']
        name = request.form['name']
        phone = request.form['phone']
        role = request.form['role_user']
        session['username_profile'] = name
        session['phone'] = phone
        session['role'] = role
        sql = connect.connection.cursor()
        sql.execute('UPDATE account, user_profile SET account.user = %s, user_profile.username_profile = %s, user_profile.phone_profile = %s WHERE account.id = %s AND user_profile.id_profile = %s ',(role,name,phone,id_user,id_user,))
        connect.connection.commit()
        sql.close()
    return redirect(url_for('account'))
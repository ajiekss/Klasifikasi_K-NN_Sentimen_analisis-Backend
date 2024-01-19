from flask import render_template, redirect, url_for, request, session, jsonify
from flask_mysqldb import MySQL
from app.config.config import run_db
from app import app
import MySQLdb.cursors
import os

app.secret_key = os.urandom(12).hex()
app.config.from_object(run_db)

connect = MySQL()

@app.route('/updateJudul', methods=['GET','POST'])
def updateJudul():
    if request.method == 'POST' and 'judul' in request.form:
        judul = request.form['judul']
        session['dataJudul'] = judul
        sql = connect.connection.cursor()
        sql.execute("UPDATE home_frontend SET judul=%s WHERE id=%s", (judul,session['id'],))
        connect.connection.commit()
    
        return redirect(url_for('frontend'))
    return redirect(url_for('frontend'))
    

@app.route('/updateSubjudul', methods=['GET', 'POST'])
def updateSubjudul():
    if request.method == 'POST':
        subjudul = request.form['subjudul']
        session['subJudul'] = subjudul 

        sql = connect.connection.cursor()
        sql.execute("UPDATE home_frontend SET subjudul=%s WHERE id=%s", (subjudul,session['id'],))
        connect.connection.commit()
        sql.close()

    return redirect(url_for('frontend'))

@app.route('/dataType', methods=['GET','POST'])
def dataType():
    if request.method == 'POST':
        dataType = request.form['datatype']
        session['dataType'] = dataType

        sql = connect.connection.cursor()
        sql.execute("UPDATE home_frontend SET dataType = %s WHERE id = %s",(dataType,session['id'],))
        connect.connection.commit()

        return redirect(url_for('frontend'))
    return redirect(url_for('frontend'))
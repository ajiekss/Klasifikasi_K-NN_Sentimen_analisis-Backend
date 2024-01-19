from flask import render_template, redirect, url_for, jsonify
from app import app
from flask_mysqldb import MySQL
from flask_cors import CORS
from app.config.config import run_db
from app.config.connect_db import Account
import MySQLdb.cursors
import os


app.secret_key = os.urandom(12).hex()
app.config.from_object(run_db)

CORS(app, resources={r'/*': {'origins': '*'}})

connect = MySQL()


@app.route('/Judul', methods=['GET','POST'])
def judul():
    sql = connect.connection.cursor(MySQLdb.cursors.DictCursor)
    sql.execute('SELECT * FROM home_frontend')
    result = sql.fetchall()
    sql.close()
    return jsonify({'dataJudul': result})

@app.route('/Footer', methods=['GET','POST'])
def footer():
    sql = connect.connection.cursor(MySQLdb.cursors.DictCursor)
    sql.execute('SELECT * FROM user_profile')
    result = sql.fetchall()
    sql.close()
    return jsonify({'dataFooter': result})

@app.route('/LS', methods=["GET","POST"])
def LS():
    sql = connect.connection.cursor(MySQLdb.cursors.DictCursor)
    sql.execute('SELECT * FROM user_profile')
    result = sql.fetchall()
    sql.close()
    return jsonify({'data': result})
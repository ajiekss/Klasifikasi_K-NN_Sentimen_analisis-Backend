import mysql.connector
import pandas as pd

connect = mysql.connector.connect(host='127.0.0.1', database='pro-leni', user='root', password='')

class Account:
    connect = connect.cursor()
    connect.execute('select account.id, user_profile.id_profile, user_profile.username_profile, account.username, account.email,account.password ,user_profile.phone_profile, user_profile.image, account.user from account Inner join user_profile on account.id = user_profile.id_profile')
    account = connect.fetchall()

class home_frontend:
    connect = connect.cursor()
    connect.execute('select * from home_frontend')
    h_frontend = connect.fetchall()

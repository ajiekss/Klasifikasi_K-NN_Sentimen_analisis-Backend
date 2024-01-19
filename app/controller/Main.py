from flask import render_template, request, jsonify, session, redirect
from app import app
from app.config.connect_db import Account
import pandas as pd

@app.route('/')
def home():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Home"
    account = Account.account
    return render_template('index.html', activeHm = active,   account=account, title=title)

@app.route('/account')
def account():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Account"
    account = Account.account
    return render_template('includes/Settings/Profile.html', activeAc=active, account=account, title=title)

@app.route('/frontend')
def frontend():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Setting Frontend"
    account = Account.account
    return render_template('includes/Settings/Frontend.html', activeFr=active,  account=account, title=title)

@app.route('/scraping')
def scrapping():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Scraping"
    account = Account.account
    return render_template('includes/Scraping.html', activeSc=active,  account=account, title=title)

@app.route('/preprocessing')
def preprocessing():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Preprocessing"
    account = Account.account
    return render_template('includes/Preprocessing.html', activePre=active,  account=account, title=title)

@app.route('/sentimen')
def sentimen():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Sentimen"
    account = Account.account
    return render_template('includes/Sentimen.html', activeSe=active,  account=account, title=title)

@app.route('/smote')
def smote():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Smote"
    account = Account.account
    return render_template('includes/Smote.html', activeSmote=active,  account=account, title=title)

@app.route('/klasifikasi')
def klasifikasi():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Klasifikasi"
    account = Account.account
    return render_template('includes/Klasifikasi.html', activeKlasifikasi=active,  account=account, title=title)

@app.route('/Data-Awal')
def DataAwal():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Data Awal"
    account = Account.account
    return render_template('includes/DataAwal/DataAwal.html', activeDA=active,  account=account, title=title)

@app.route('/Data-Preprocessing')
def DataPre():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Data Preprocessing"
    account = Account.account
    return render_template('includes/DataPre/DataPre.html', activeDP=active,  account=account, title=title)

@app.route('/Step-Data-Preprocessing')
def StepDataPre():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Step Data Preprocessing"
    account = Account.account
    return render_template('includes/StepDataPre/StepDataPre.html', activeSDP=active,  account=account, title=title)

@app.route('/Data-Sentimen')
def DataSen():
    if not session.get('loggedin'):
        return redirect('/login')
    active = "active"
    title = "Data Sentimen"
    account = Account.account
    return render_template('includes/DataSen/DataSen.html', activeDS=active,  account=account, title=title)
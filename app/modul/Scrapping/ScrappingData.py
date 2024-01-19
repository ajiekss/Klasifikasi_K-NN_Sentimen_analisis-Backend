from flask import request, redirect, url_for, jsonify, render_template
from google_play_scraper import reviews_all, Sort
from flask_cors import CORS
from app.config.config import run_db
from app import app
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
import os

# app.secret_key = os.urandom(12).hex()
app.config.from_object(run_db)

connect = MySQL(app)

class dataScraping:
    def __init__(self, name):
        self.name = name

    def ProcesScraping(self):
        data = reviews_all(
            ''+self.name,
            sleep_milliseconds=0,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            )
        dataScr = pd.DataFrame(data)
        dataScr.drop(columns={'reviewId', 'userImage','thumbsUpCount', 'reviewCreatedVersion', 'replyContent', 'repliedAt'},inplace = True)
        return dataScr


@app.route('/ScrapingData', methods=['GET','POST'])
def ScrapingData():
    msg = 'Success'
    dataScrA = []
    if request.method == "POST":
        post_data = request.get_json(silent=True)
        dataScr = post_data.get('kata_kunci')
        nama = dataScraping(dataScr)
        scraping = nama.ProcesScraping()
        Listarray = np.array(scraping).tolist()
        jumlahData = len(Listarray)
        # jumlahData = "200"
        return jsonify({'data':msg,'JumlahData': jumlahData, 'dataScrGP': Listarray})
    return jsonify({'data':msg, 'dataScr' : dataScrA})
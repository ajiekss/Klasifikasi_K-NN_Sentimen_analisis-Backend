from flask import jsonify
from app.modul.Data.dbmodel import DBModel
from app import app
from flask_cors import CORS
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/DataA', methods=['GET','POST'])
def dataA():
    dbmodel = DBModel()
    resultDA = dbmodel.get_data_all("pro-Leni","DataAwal")
    data = pd.DataFrame(resultDA)
    dataDA = np.array(data)
    return jsonify({'data': dataDA.tolist(), 'jumlahData': len(data)})

@app.route('/DataP', methods=['GET','POST'])
def dataP():
    dbmodel = DBModel()
    resultDP = dbmodel.get_data_all("pro-Leni","DataPreprocess")
    data = pd.DataFrame(resultDP)
    data = data[['No','Username','Score','At','Ulasan','Ulasan_tokens','Ulasan_tokens_WSW','Ulasan_normalized','Ulasan_normalized_term']]
    dataDP = np.array(data)
    return jsonify({'data': dataDP.tolist(), 'jumlahData': len(data)})

@app.route('/StepDataP', methods=['GET','POST'])
def StepdataP():
    dbmodel = DBModel()
    resultDP = dbmodel.get_data_all("pro-Leni","StepDataPreprocess")
    data = pd.DataFrame(resultDP)
    dataSDP = np.array(data)
    return jsonify({'data': dataSDP.tolist()})

@app.route('/DataS', methods=['GET','POST'])
def dataS():
    dbmodel = DBModel()
    resultDS = dbmodel.get_data_all("pro-Leni","DataSentimen")
    data = pd.DataFrame(resultDS)
    fig, axes = plt.subplots()
    sns.histplot(data=data,x='Ulasan_normalized_term_SentL',hue="Ulasan_normalized_term_SentL",ax=axes)
    fig.savefig('app/static/imagePlotSen/my_plot.png')
    plt.close()
    dataDS = np.array(data)
    return jsonify({'data': dataDS.tolist()})
from flask import jsonify, request, render_template
from app import app
from flask_cors import CORS
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from app.modul.Smote.dbmodel import DBModel
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

encode = LabelEncoder()

class PlotDataA:
    def __init__(self,data):
        self.data = data
    
    def PlotdataA(self):
        data = self.data
        positive = data[data['Ulasan_normalized_term_SentL'] == 'positive']['label'].count()
        neutral = data[data['Ulasan_normalized_term_SentL'] == 'neutral']['label'].count()
        negative = data[data['Ulasan_normalized_term_SentL'] == 'negative']['label'].count()

        labels = ['positive neutral negative']
        pos = [positive]
        neu = [neutral]
        neg = [negative]

        x = np.arange(len(labels)) 
        width = 1 

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/1, pos, width, label='Positive')
        rects2 = ax.bar(x + width/2, neu, width, label='Neutral')
        rects3 = ax.bar(x - width/3, neg, width, label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Jumlah')
        ax.set_title('Data Awal')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)
        
        path = 'app/static/imagePlotSen/DataAwal/DataAwal.png'
        fig.savefig(path)
        datapath = path.split('/')
        return datapath[4]

class PlotDataS:
    def __init__(self,data):
        self.data = data

    def PlotdataS(self):
        data = self.data
        positive = data[data['labelAngka'] == 1 ]['label'].count()
        neutral = data[data['labelAngka'] == 0 ]['label'].count()
        negative = data[data['labelAngka'] == -1 ]['label'].count()

        labels = ['positive neutral negative']
        pos = [positive]
        neu = [neutral]
        neg = [negative]

        x = np.arange(len(labels)) 
        width = 1 

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/1, pos, width, label='Positive')
        rects2 = ax.bar(x + width/2, neu, width, label='Neutral')
        rects3 = ax.bar(x - width/3, neg, width, label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Jumlah')
        ax.set_title('Data Smote')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)
        
        path = 'app/static/imagePlotSen/DataSmote/DataSmote.png'
        fig.savefig(path)
        datapath = path.split('/')
        return datapath[4]

class PlotDataO:
    def __init__(self,data):
        self.data = data

    def PlotdataO(self):
        data = self.data
        positive = data[data['labelAngka'] == 1 ]['label'].count()
        neutral = data[data['labelAngka'] == 0 ]['label'].count()
        negative = data[data['labelAngka'] == -1 ]['label'].count()

        labels = ['positive neutral negative']
        pos = [positive]
        neu = [neutral]
        neg = [negative]

        x = np.arange(len(labels)) 
        width = 1 

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/1, pos, width, label='Positive')
        rects2 = ax.bar(x + width/2, neu, width, label='Neutral')
        rects3 = ax.bar(x - width/3, neg, width, label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Jumlah')
        ax.set_title('Data Over')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)

        path = 'app/static/imagePlotSen/DataOver/DataOver.png'
        fig.savefig(path)
        datapath = path.split('/')
        return datapath[4]

class PlotDataU:
    def __init__(self,data):
        self.data = data
    
    def PlotdataU(self):
        data = self.data
        positive = data[data['labelAngka'] == 1 ]['label'].count()
        neutral = data[data['labelAngka'] == 0 ]['label'].count()
        negative = data[data['labelAngka'] == -1 ]['label'].count()

        labels = ['positive neutral negative']
        pos = [positive]
        neu = [neutral]
        neg = [negative]

        x = np.arange(len(labels)) 
        width = 1 

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/1, pos, width, label='Positive')
        rects2 = ax.bar(x + width/2, neu, width, label='Neutral')
        rects3 = ax.bar(x - width/3, neg, width, label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Jumlah')
        ax.set_title('Data Under')
        ax.set_xticks(x, labels)
        ax.legend()

        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        ax.bar_label(rects3, padding=3)

        path = 'app/static/imagePlotSen/DataUnder/DataUnder.png'
        fig.savefig(path)
        datapath = path.split('/')
        return datapath[4]

def text_transformS(df):
    df['Ulasan_normalized_term'] = encode.fit_transform(df['Ulasan_normalized_term'].values)
    x = df[['Ulasan_normalized_term']]
    y = df[['label']]
    over = SMOTE(random_state=42)
    x_sampling, y_sampling = over.fit_resample(x,y)
    x_sampling['Ulasan_normalized_term'] = list(encode.inverse_transform(x_sampling['Ulasan_normalized_term'].values))
    data = x_sampling.join(y_sampling)
    return data

def text_transformO(df):
    df['Ulasan_normalized_term'] = encode.fit_transform(df['Ulasan_normalized_term'].values)
    x = df[['Ulasan_normalized_term']]
    y = df[['label']]
    over = RandomOverSampler(random_state=42)
    x_sampling, y_sampling = over.fit_resample(x,y)
    x_sampling['Ulasan_normalized_term'] = list(encode.inverse_transform(x_sampling['Ulasan_normalized_term'].values))
    data = x_sampling.join(y_sampling)
    return data

def text_transformU(df):
    df['Ulasan_normalized_term'] = encode.fit_transform(df['Ulasan_normalized_term'].values)
    x = df[['Ulasan_normalized_term']]
    y = df[['label']]
    over = RandomUnderSampler(random_state=42)
    x_sampling, y_sampling = over.fit_resample(x,y)
    x_sampling['Ulasan_normalized_term'] = list(encode.inverse_transform(x_sampling['Ulasan_normalized_term'].values))
    data = x_sampling.join(y_sampling)
    return data

class SentimenLabelSOU:
    def __init__(self,data):
        self.data = data
    
    def sentimenLabel(self):
        data = self.data
        resultDrop = data
        resultDrop['label'] = resultDrop['label'].replace({1 : 'positive'}).replace({0 : 'neutral'}).replace({-1 : 'negative'})
        resultDrop['labelAngka'] = resultDrop['label'].replace({'positive': 1}).replace({'neutral': 0}).replace({'negative': -1})
        return resultDrop
    
class SentimenLabel:
    def __init__(self,data):
        self.data = data
    
    def sentimenLabel(self):
        data = self.data
        resultDrop = data.drop(columns=['Ulasan_tokens','Ulasan_tokens_WSW','Ulasan_normalized'])
        resultDrop['label'] = resultDrop['Ulasan_normalized_term_SentL'].replace({'positive': 1}).replace({'neutral': 0}).replace({'negative': -1})
        dbmodel = DBModel()
        dbmodel.insert_data('pro-Leni','DataLabelAngka', resultDrop)
        return resultDrop

        
def smote(data):
    data = text_transformS(data)
    labelH = SentimenLabelSOU(data)
    dataL = labelH.sentimenLabel()
    # print(dataL)
    dbmodel = DBModel()
    insert_data = dbmodel.insert_data('pro-Leni','DataSmote', dataL)
    return dataL

def over(data):
    data = text_transformO(data)
    labelH = SentimenLabelSOU(data)
    dataL = labelH.sentimenLabel()
    dbmodel = DBModel()
    insert_data = dbmodel.insert_data('pro-Leni','DataOver', dataL)
    return dataL
    
def under(data):
    data = text_transformU(data)
    labelH = SentimenLabelSOU(data)
    dataL = labelH.sentimenLabel()
    # print(dataL)
    dbmodel = DBModel()
    insert_data = dbmodel.insert_data('pro-Leni','DataUnder', dataL)
    return dataL


@app.route('/Smote', methods=['POST','GET'])
def Smote():
    data = []
    if request.method == "POST":
        post_data = request.get_json(silent=True)
        dataName = post_data.get('name')
        dbmodel = DBModel()
        dataB = dbmodel.get_data_all('pro-Leni','DataSentimen')
        dF = pd.DataFrame(dataB)
        dataLabel = SentimenLabel(dF)
        #Data Awal
        resultDataLabel = dataLabel.sentimenLabel()
        resultDataLabelS = dataLabel.sentimenLabel()
        resultDataLabelO = dataLabel.sentimenLabel()
        resultDataLabelU = dataLabel.sentimenLabel()
        dbmodel = DBModel()
        insert_data = dbmodel.insert_data('pro-Leni','DataAwalSmote', resultDataLabel)
        dataSa = np.array(resultDataLabel).tolist()
        pltDa = PlotDataA(resultDataLabel)
        dataPathA = pltDa.PlotdataA()
        # Semote
        SsData = smote(resultDataLabelS)
        pltSs = PlotDataS(SsData)
        dataPathS = pltSs.PlotdataS()
        dataSs = np.array(SsData).tolist()
        # Over
        SoData = over(resultDataLabelO)
        pltSo = PlotDataO(SoData)
        dataPathO = pltSo.PlotdataO()
        dataSo = np.array(SoData).tolist()
        # Under
        UuData = under(resultDataLabelU)
        pltUu = PlotDataU(UuData)
        dataPathU = pltUu.PlotdataU()
        dataSu = np.array(UuData).tolist()
        dataPath = [{'DA': dataPathA, 'DS': dataPathS, 'DO': dataPathO, 'DU': dataPathU}]
        dataSemua = [{'dataSa': dataSa,'dataSs':dataSs, 'dataSo': dataSo, 'dataSu': dataSu }]
        return jsonify({'data': dataSemua, 'dataPath': dataPath})
    return jsonify({'data': data})
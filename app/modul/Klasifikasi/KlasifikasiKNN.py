from flask import jsonify, request
from app import app
from app.modul.Klasifikasi.dbmodel import DBModel
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer , CountVectorizer
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from flask_cors import CORS
from localStoragePy import localStoragePy
import numpy as np
import pandas as pd
import re
import warnings
import math
warnings.filterwarnings("ignore")

CORS(app, resources={r'/*': {'origins': '*'}})

encode = LabelEncoder()

localStorage = localStoragePy('nilaiK','json')

class repleaces_casefoldKK:
    def __init__(self, replaces):
        self.replaces = replaces
    
    def Replace_CasefoldKK(self):
        symbols = "0123456789!\"#$%&()*+-.'/:;<=>?@[\]^_`{|}~\n"
        repleacess = re.sub('[%s]' %(symbols),'',self.replaces)
        return repleacess.casefold()
    
class percabangan:
    def __init__(self, percabangan):
        self.data = percabangan

    def Percabangan(self):
        data = self.data
        if data == [1]:
            dataText = "Positive"
        elif data == [0]:
            dataText = "Neutral"
        elif data == [-1]:
            dataText = "Negative"
        return dataText

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

class klasifikasi_data:
    def __init__(self, name, nilaiK):
        self.name = name
        self.nilaiK = int(nilaiK)
        print(self.nilaiK)
    
    def DataA(self):
        dbmodel = DBModel()
        dataDB = dbmodel.get_data_all('pro-Leni','DataAwalSmote')
        data = pd.DataFrame(dataDB)
        lenData = len(data)
        x = data['Ulasan_normalized_term']
        y = data['label']
        vectorize = CountVectorizer(min_df=1)
        response = vectorize.fit_transform(x).toarray()
        X_train, X_test, y_train, y_test = train_test_split(response, y, test_size=0.2, random_state=42)
        classifier = KNeighborsClassifier(n_neighbors=self.nilaiK)
        classifier.fit(X_train, y_train) 
        predictions = classifier.predict(X_test)
        Accuracy_Score = accuracy_score(predictions, y_test)*100
        print("Hasil Akurasi Data Awal : ", Accuracy_Score)

        # klasifikasi
        dataKata_kunci = repleaces_casefoldKK(self.name)
        kata_kunci = dataKata_kunci.Replace_CasefoldKK()
        KK_response = vectorize.transform([kata_kunci]).toarray()
        result = classifier.predict(KK_response)
        data = percabangan(result)
        print(data.Percabangan())
        resultData = [{'dataLabel': data.Percabangan(), 'dataAkurasi' : round(Accuracy_Score), 'lenData': lenData}]
        return resultData
    
    def DataS(self):
        dbmodel = DBModel()
        dataDB = dbmodel.get_data_all('pro-Leni','DataAwalSmote')
        data = pd.DataFrame(dataDB)
        dataEncode = text_transformS(data)
        lenData = len(dataEncode)
        x = dataEncode['Ulasan_normalized_term']
        y = dataEncode['label']
        vectorize = CountVectorizer(min_df=1)
        response = vectorize.fit_transform(x).toarray()
        X_train, X_test, y_train, y_test = train_test_split(response, y, test_size=0.2, random_state=42)
        classifier = KNeighborsClassifier(n_neighbors=self.nilaiK)
        classifier.fit(X_train, y_train) 
        predictions = classifier.predict(X_test)
        Accuracy_Score = accuracy_score(predictions, y_test)*100
 
        # klasifikasi
        dataKata_kunci = repleaces_casefoldKK(self.name)
        kata_kunci = dataKata_kunci.Replace_CasefoldKK()
        KK_response = vectorize.transform([kata_kunci]).toarray()
        result = classifier.predict(KK_response)
        data = percabangan(result)
        print(data.Percabangan())
        resultData = [{'dataLabel': data.Percabangan(), 'dataAkurasi' : round(Accuracy_Score), 'lenData': lenData}]
        return resultData
    
    def DataO(self):
        dbmodel = DBModel()
        dataDB = dbmodel.get_data_all('pro-Leni','DataAwalSmote')
        data = pd.DataFrame(dataDB)
        dataEncode = text_transformO(data)
        lenData = len(dataEncode)
        x = dataEncode['Ulasan_normalized_term']
        y = dataEncode['label']
        vectorize = CountVectorizer(min_df=1)
        response = vectorize.fit_transform(x).toarray()
        X_train, X_test, y_train, y_test = train_test_split(response, y, test_size=0.2, random_state=42)
        classifier = KNeighborsClassifier(n_neighbors=self.nilaiK)
        classifier.fit(X_train, y_train) 
        predictions = classifier.predict(X_test)
        Accuracy_Score = accuracy_score(predictions, y_test)*100

        # klasifikasi
        dataKata_kunci = repleaces_casefoldKK(self.name)
        kata_kunci = dataKata_kunci.Replace_CasefoldKK()
        KK_response = vectorize.transform([kata_kunci]).toarray()
        result = classifier.predict(KK_response)
        data = percabangan(result)
        print(data.Percabangan())
        resultData = [{'dataLabel': data.Percabangan(), 'dataAkurasi' :round(Accuracy_Score), 'lenData': lenData}]
        return resultData
    
    def DataU(self):
        dbmodel = DBModel()
        dataDB = dbmodel.get_data_all('pro-Leni','DataAwalSmote')
        data = pd.DataFrame(dataDB)
        dataEncode = text_transformU(data)
        lenData = len(dataEncode)
        x = dataEncode['Ulasan_normalized_term']
        y = dataEncode['label']
        vectorize = CountVectorizer(min_df=1)
        response = vectorize.fit_transform(x).toarray()
        X_train, X_test, y_train, y_test = train_test_split(response, y, test_size=0.2, random_state=42)
        classifier = KNeighborsClassifier(n_neighbors=self.nilaiK)
        classifier.fit(X_train, y_train) 
        predictions = classifier.predict(X_test)
        Accuracy_Score = accuracy_score(predictions, y_test)*100
 
        # klasifikasi
        dataKata_kunci = repleaces_casefoldKK(self.name)
        kata_kunci = dataKata_kunci.Replace_CasefoldKK()
        KK_response = vectorize.transform([kata_kunci]).toarray()
        result = classifier.predict(KK_response)
        data = percabangan(result)
        print(data.Percabangan())
        resultData = [{'dataLabel': data.Percabangan(), 'dataAkurasi' : round(Accuracy_Score), 'lenData': lenData}]
        return resultData

def nilaiN(nilaiK):
    dbmodel = DBModel()
    dbmodel.insert_data('pro-Leni', 'nilaiK', nilaiK)
    inputK = dbmodel.get_data_all('pro-Leni','nilaiK')
    inputK = pd.DataFrame(inputK)
    dataK = inputK['nilaiK'].tolist()
    data = "".join(dataK)
    return int(data)

def nilaiNApi():
    dbmodel = DBModel()
    dbinputK = dbmodel.get_data_all('pro-Leni','nilaiK')
    inputK = pd.DataFrame(dbinputK)
    dataK = inputK['nilaiK'].tolist()
    data = "".join(dataK)
    return int(data)

@app.route('/KlasifikasiKNN', methods=['GET','POST'])
def klasifikasiKNN():
    data=[]
    if request.method == "POST":
        key = request.get_json(silent=True)
        dataKey = key.get('KataKunci') 
        nilaiK = key.get('nilaiK')
        nilaiK = {'nilaiK': nilaiK}
        inputK = nilaiN(nilaiK)
        Kelasifikasi = klasifikasi_data(dataKey,inputK)
        resultDA = Kelasifikasi.DataA()
        resultDS = Kelasifikasi.DataS()
        resultDO = Kelasifikasi.DataO()
        resultDU = Kelasifikasi.DataU()
        dataSemua = [{'resultDA': resultDA, 'resultDS': resultDS, 'resultDO': resultDO, 'resultDU': resultDU}]
        # dataSemua=[]
        return jsonify({'data': dataSemua})
    return jsonify({'data': data})

@app.route('/KlasifikasiKNNApi', methods=['GET','POST'])
def klasifikasiKNNApi():
    data=[]
    if request.method == "POST":
        key = request.get_json(silent=True)
        dataKey = key.get('KataKunci') 
        inputK = nilaiNApi()
        Kelasifikasi = klasifikasi_data(dataKey,inputK)
        resultDA = Kelasifikasi.DataA()
        resultDS = Kelasifikasi.DataS()
        resultDO = Kelasifikasi.DataO()
        resultDU = Kelasifikasi.DataU()
        dataSemua = [{'resultDA': resultDA, 'resultDS': resultDS, 'resultDO': resultDO, 'resultDU': resultDU}]
        # dataSemua=[]
        return jsonify({'data': dataSemua})
    return jsonify({'data': data})
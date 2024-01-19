from flask import render_template, redirect, url_for, jsonify, request
from app import app
from app.modul.Sentimen.dbmodel import DBModel
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from werkzeug.utils import secure_filename
from multiprocessing import Process
import pandas as pd
import numpy as np
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'xlsx', 'csv', 'png', 'jpg', 'jpeg', 'gif'}

class sentimenDt():
    def __init__(self, data):
        self.data = data

    def SentimenData(self):
        dataSenA = []
        data = self.data
        for i in data:
            dataSenA.append(i)
        dataSen = pd.DataFrame(dataSenA)
        def SentimenLabel(text):
            pretrained= "mdhugol/indonesia-bert-sentiment-classification"
            model = AutoModelForSequenceClassification.from_pretrained(pretrained)
            tokenizer = AutoTokenizer.from_pretrained(pretrained)
            sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
            label_index = {'LABEL_0': 'positive', 'LABEL_1': 'neutral', 'LABEL_2': 'negative'}
            result = sentiment_analysis(text)
            status = label_index[result[0]['label']]
            print(status)
            return status
        
        dataSen['Ulasan_normalized_term_SentL'] = dataSen['Ulasan_normalized_term'].apply(SentimenLabel)

        return dataSen


@app.route('/Sentimen', methods=['GET','POST'])
def Sentimen():
    data =[]
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        dataSen = post_data.get('name')
        dbmodel = DBModel()
        getData = dbmodel.get_data_all("pro-Leni", "DataPreprocess")
        data = sentimenDt(getData)
        if dataSen == 'Start':
            dataSentimen = data.SentimenData()
            dataSentimen.to_excel('app/modul/Sentimen/Sentimen.xlsx', index=False)
            # insertData = dbmodel.insert_data("pro-Leni", "DataSentimen", dataSentimen)
            # resultDataSenh = pd.DataFrame(dataSentimen)
            # resultDataSen = np.array(resultDataSenh).tolist()
            return jsonify({'data': 'Start'})
        if dataSen == 'Stop':
            process = Process(target=data.SentimenData())
            process.terminate()
            return jsonify({'data': 'Stop'})  
    return jsonify({'data': data})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Alternatif_Sentimen', methods=['GET','POST'])
def Alternatif_Sentimen():
    data = []
    if request.method == "POST":
        file = request.files['dataFile']
        if file.filename == '':
            name = 'No selected file'
            return jsonify({'error': name})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = 'app/Data/AlternativeData'
            file.save(os.path.join(path, 'Sentimen.xlsx'))
            pathOpen = 'app/Data/AlternativeData/Sentimen.xlsx'
            fileXlsx = pd.read_excel(pathOpen, skiprows=1)
            nameColumn = fileXlsx.columns
            listColumns = list(nameColumn)
            if 'No' and 'Username' and 'Score' and 'At' and 'Ulasan' and 'Ulasan_tokens' and 'Ulasan_tokens_WSW' and 'Ulasan_normalized' and 'Ulasan_normalized_term' and 'Ulasan_normalized_term_SentL' in listColumns:
                modeldb = DBModel()
                modeldb.insert_data("pro-Leni","DataSentimen", fileXlsx)
                return jsonify({'data': 'success'})
            else:
                return jsonify({'data': 'error'})
    return jsonify({"data": data})
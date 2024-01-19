from flask import flash, url_for, request, render_template, jsonify, redirect
from werkzeug.utils import secure_filename
from app import app
from app.modul.Preprocessing.dbmodel import DBModel
from app.config.connect_db import Account
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import pandas as pd
import string
import re
import os

UPLOAD_FOLLDER = 'app/Data'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'xlsx', 'csv', 'png', 'jpg', 'jpeg', 'gif'}

class PreprocessingData:
    def __init__(self, fileXlsx):
        self.File = fileXlsx

    def Preprocessing(self):
        file = self.File

        def deEmojify(text):
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        
        file['Ulasan'] = file['Ulasan'].apply(deEmojify)

        # case folding
        file['Ulasan'] = file['Ulasan'].str.lower()

        def remove_tweet_special(text):
            # remove tab, new line, ans back slice
            text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
            # remove non ASCII (emoticon, chinese word, .etc)
            text = text.encode('ascii', 'replace').decode('ascii')
            # remove mention, link, hashtag
            text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
            # koreksi duplikasi tiga karakter beruntun atau lebih (contoh. yukkk)
            text = re.sub(r'([a-zA-Z])\1\1','\\1', text)
            # remove incomplete URL
            return text.replace("http://", " ").replace("https://", " ")
        
        file['Ulasan'] = file['Ulasan'].apply(remove_tweet_special)

        # remove punctuatuation
        def remove_punctuation(text):
            return text.translate(str.maketrans("","",string.punctuation))
        
        file['Ulasan'] = file['Ulasan'].apply(remove_punctuation)

        # remove Number
        def remove_number(text):
            return  re.sub(r"\d+", "", text)

        file['Ulasan'] = file['Ulasan'].apply(remove_number)

        #remove whitespace leading & trailing
        def remove_whitespace_LT(text):
            return text.strip()
        
        file['Ulasan'] = file['Ulasan'].apply(remove_whitespace_LT)

        #remove multiple whitespace into single whitespace
        def remove_whitespace_multiple(text):
            return re.sub('\s+',' ',text)

        file['Ulasan'] = file['Ulasan'].apply(remove_whitespace_multiple)

        # remove single char
        def remove_singl_char(text):
            return re.sub(r"\b[a-zA-Z]\b", "", text)
        
        file['Ulasan'] = file['Ulasan'].apply(remove_singl_char)

        # NLTK word rokenize 
        def word_tokenize_wrapper(text):
            return word_tokenize(text)

        file['Ulasan_tokens'] = file['Ulasan'].apply(word_tokenize_wrapper)


        # def freqDist_wrapper(text):
        #     return FreqDist(text)

        # file['Ulasan_tokens_fdist'] = file['Ulasan_tokens'].apply(freqDist_wrapper)

        # get stopword indonesia
        list_stopwords = stopwords.words('indonesian')

        list_stopwords.extend(["yg", "dg", "dgn", "ny", "d", 'klo', 
                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh',
                       '&amp', 'yah'])
        
        txt_stopword = pd.read_csv("app/modul/Preprocessing/stopwords.txt", names= ["stopwords"], header = None)

        list_stopwords.extend(txt_stopword["stopwords"][0].split(' '))

        list_stopwords = set(list_stopwords)

        def stopwords_removal(words):
            return [word for word in words if word not in list_stopwords]

        file['Ulasan_tokens_WSW'] = file['Ulasan_tokens'].apply(stopwords_removal) 

        normalizad_word = pd.read_excel("app/modul/Preprocessing/normalisasi.xlsx")

        normalizad_word_dict = {}

        for index, row in normalizad_word.iterrows():
            if row[0] not in normalizad_word_dict:
                normalizad_word_dict[row[0]] = row[1] 

        def normalized_term(document):
            return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

        file['Ulasan_normalized'] = file['Ulasan_tokens_WSW'].apply(normalized_term)


        def list_normalized(document):
            return " ".join(document)
        
        file['Ulasan_normalized_term'] = file['Ulasan_normalized'].apply(list_normalized)

        return file
    
class StepsPreData:
    def __init__(self, fileXlsx):
        self.File = fileXlsx

    def StepPreprocessing(self):
        file = self.File
        preFile = file.drop(columns=['No','Username','Score','At'])

        def deEmojify(text):
            regrex_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags = re.UNICODE)
            return regrex_pattern.sub(r'',text)
        
        preFile['Ulasan'] = preFile['Ulasan'].apply(deEmojify)

        def Lower(text):
            return text.casefold()

        # case folding
        preFile['lower'] = preFile['Ulasan'].apply(Lower)

        def remove_tweet_special(text):
            # remove tab, new line, ans back slice
            text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
            # remove non ASCII (emoticon, chinese word, .etc)
            text = text.encode('ascii', 'replace').decode('ascii')
            # remove mention, link, hashtag
            text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
            # koreksi duplikasi tiga karakter beruntun atau lebih (contoh. yukkk)
            text = re.sub(r'([a-zA-Z])\1\1','\\1', text)
            # remove incomplete URL
            return text.replace("http://", " ").replace("https://", " ")
        
        preFile['remove_special'] = preFile['lower'].apply(remove_tweet_special)

        # remove Number
        def remove_number(text):
            return  re.sub(r"\d+", "", text)

        preFile['remove_number'] = preFile['remove_special'].apply(remove_number)

        # remove punctuatuation
        def remove_punctuation(text):
            return text.translate(str.maketrans("","",string.punctuation))
        
        preFile['remove_punctuation'] = preFile['remove_number'].apply(remove_punctuation)


        #remove whitespace leading & trailing
        def remove_whitespace_LT(text):
            return text.strip()
        
        preFile['remove_punctuation'] = preFile['remove_punctuation'].apply(remove_whitespace_LT)

        #remove multiple whitespace into single whitespace
        def remove_whitespace_multiple(text):
            return re.sub('\s+',' ',text)

        preFile['remove_punctuation'] = preFile['remove_punctuation'].apply(remove_whitespace_multiple)

        # remove single char
        def remove_singl_char(text):
            return re.sub(r"\b[a-zA-Z]\b", "", text)
        
        preFile['remove_punctuation'] = preFile['remove_punctuation'].apply(remove_singl_char)

        # NLTK word tokenize 
        def word_tokenize_wrapper(text):
            return word_tokenize(text)

        preFile['tokenization'] = preFile['remove_punctuation'].apply(word_tokenize_wrapper)


        # get stopword indonesia
        list_stopwords = stopwords.words('indonesian')

        list_stopwords.extend(["yg", "dg", "dgn", "ny", "d", 'klo', 
                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh',
                       '&amp', 'yah'])
        
        txt_stopword = pd.read_csv("app/modul/Preprocessing/stopwords.txt", names= ["stopwords"], header = None)

        list_stopwords.extend(txt_stopword["stopwords"][0].split(' '))

        list_stopwords = set(list_stopwords)

        def stopwords_removal(words):
            return [word for word in words if word not in list_stopwords]

        preFile['remove_stopword'] = preFile['tokenization'].apply(stopwords_removal) 

        
        # normalisasi
        normalizad_word = pd.read_excel("app/modul/Preprocessing/normalisasi.xlsx")

        normalizad_word_dict = {}

        for index, row in normalizad_word.iterrows():
            if row[0] not in normalizad_word_dict:
                normalizad_word_dict[row[0]] = row[1] 

        def normalized_term(document):
            return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

        preFile['normalisasi'] = preFile['remove_stopword'].apply(normalized_term)

        def list_normalized(document):
            return " ".join(document)
        
        preFile['normalisasi'] = preFile['normalisasi'].apply(list_normalized)

        return preFile


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadData', methods=["GET", "POST"])
def uploadData():
    data = []
    if request.method == "POST":
        file = request.files['dataFile']
        if file.filename == '':
            name = 'No selected file'
            return jsonify({'error': name})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = filename
            return jsonify({"data": file})
    return jsonify({"data": data})

@app.route('/ProsesP', methods=['GET', 'POST'])
def prosesP():
    data = []
    if request.method == "POST":
        name = request.form['name']
        nama = name.split(".")
        if nama[1] == 'xlsx':
            path ='app/Data/'+name
            fileXlsx = pd.read_excel(path, skiprows=1)
            fileXlsxStep = pd.read_excel(path, skiprows=1)
            modeldb = DBModel()
            result_insert_table_Awal = modeldb.insert_data("pro-Leni","DataAwal", fileXlsx)
            #preprocessing
            ResultPre = PreprocessingData(fileXlsx)
            ResultR = ResultPre.Preprocessing()
            ResultR.to_excel('app/modul/Preprocessing/noEndprepross.xlsx', index=False)
            # readExcel and dropna()
            dataRE = pd.read_excel('app/modul/Preprocessing/noEndprepross.xlsx')
            result =dataRE.dropna()
            dbmodel = DBModel()
            dbmodel.insert_data("pro-Leni", "DataPreprocess", result)
            #StepPreData
            StepResultPre = StepsPreData(fileXlsxStep)
            StepResultR = StepResultPre.StepPreprocessing()
            StepResultR.to_excel('app/modul/Preprocessing/StepnoEndprepross.xlsx', index=False)
            dataSPE= pd.read_excel('app/modul/Preprocessing/StepnoEndprepross.xlsx')
            Stepresult = dataSPE.dropna()
            dbmodel = DBModel()
            dbmodel.insert_data("pro-Leni", "StepDataPreprocess", Stepresult)

            account = Account.account
            active = "active"
            title = "Preprocessing"
            msg = "Berhasil"
            return render_template('includes/Preprocessing.html', account=account ,tables=[result.to_html(classes='table table-bordered',table_id="dataPre", index=False)], activePre=active, title=title, msg=msg)
        if nama[1] == 'csv':
            path ='app/Data/'+name
            fileXlsx = pd.read_csv(path, skiprows=1)
            ResultPre = PreprocessingData(fileXlsx)
            ResultR = ResultPre.Preprocessing()
            result = pd.DataFrame(ResultR)
            active = "active"
            title = "Preprocessing"
            msg = "berhasil"
            return render_template('includes/Preprocessing.html', tables=[result.to_html(classes='table table-bordered',table_id="dataPre", index=False)], activePre=active, title=title, msg=msg)
        return jsonify({"data":data})
    return jsonify({"data": data})
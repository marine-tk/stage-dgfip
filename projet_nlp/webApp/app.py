# Importation des librairies
import flask
from flask import Flask, redirect, url_for, render_template, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import make_pipeline 
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from imblearn.over_sampling import RandomOverSampler
from tfidf import predict_reglog
from fasttext import predict_fasttext
from bert import predict_bert

# Création de l'application Flask
app = Flask(__name__)

# Index de la page
@app.route('/')
def index():
    return render_template('index.html')

# Route : TF-IDF - Régression Logistique
@app.route('/reglog', methods=['GET', 'POST'])
def reglog():
    if request.method == "POST":
        reglog = request.form.get("reglog")
        str_predict = predict_reglog(reglog)
        print(str_predict)
        str_predict = reglog + " : " + str_predict
        return render_template('reglog.html',str_predict=str_predict)
    else:
        return render_template('reglog.html')

# Route : FastText
@app.route('/fasttext', methods=['GET', 'POST'])
def fasttext():
    if request.method == "POST":
        fasttext = request.form.get("fasttext")
        str_predict = predict_fasttext(fasttext)
        print(str_predict)
        str_predict = fasttext + " : " + str_predict
        return render_template('fasttext.html',str_predict=str_predict)
    else:
        return render_template('fasttext.html')

# Route : CamemBERT
@app.route('/bert', methods=['GET', 'POST'])
def bert():
    if request.method == "POST":
        bert = request.form.get("bert")
        str_predict = predict_bert(bert)
        print(str_predict)
        str_predict = bert + " : " + str_predict
        return render_template('bert.html',str_predict=str_predict)
    else:
        return render_template('bert.html')

# Route : Nous
@app.route('/nous', methods=['GET', 'POST'])
def nous():
        return render_template('nous.html')

# Route : Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
        return render_template('nous_contacter.html')
  
# Route : Méthodologie (en cours de construction)
@app.route('/methodologie', methods=['GET', 'POST'])
def contact():
        return render_template('methodologie.html')
  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

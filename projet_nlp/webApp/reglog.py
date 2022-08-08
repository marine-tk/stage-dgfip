# Importation des librairies
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import make_pipeline 
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from imblearn.over_sampling import RandomOverSampler
from tfidf import fonction

def predict_reglog(str_pred):

    X_train = fonction()

    lr = joblib.load("model_reglog.pkl") 
    model_columns = joblib.load("model_columns_reglog.pkl") # Load "model_columns.pkl"

    query = str_pred
    data = [query, "excellente idée"]
    df = pd.DataFrame(data, columns=['Avis'])

    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    pipe.fit(X_train['Avis'])
    query = pipe.transform(df['Avis'])
    prediction = list(lr.predict(query))
    
    for i in range(len(prediction)):
        if prediction[i] == 0:
            prediction[i] = 'negatif'
        if prediction[i] == 1:
            prediction[i] = 'positif'
            
    return prediction[0]

    
    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:12:10 2022

@author: geoffroyperonne
"""

import fasttext

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix, roc_curve

import matplotlib.pyplot as plt

import seaborn as sn

from imblearn.over_sampling import RandomOverSampler

import re



def clean_str(string):

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)    
    
    string = re.sub(r"\'s", " 's", string)
    
    string = re.sub(r"\'ve", " \'ve", string)
    
    string = re.sub(r"n\'t", " n\'t", string)
    
    string = re.sub(r"\'re", " \'re", string)
    
    string = re.sub(r"\'d", " \'d", string)
    
    string = re.sub(r"\'ll", " \'ll", string)
    
    string = re.sub(r",", " , ", string)
    
    string = re.sub(r"!", " ! ", string)
    
    string = re.sub(r"\(", " ( ", string)
    
    string = re.sub(r"\)", " ) ", string)
    
    string = re.sub(r"\?", " ? ", string)
    
    string = re.sub(r"\s{2,}", " ", string)  
    
    return(string.strip().lower())




def to_text(df,filename) :
    
    cat = open('./' + filename + '.txt', 'w')
    
    for index,l in df.iterrows() :
        
        #print("Index : ",index)
        if l["Sentiment"]=="positif":
            
            cat.write('__label__positif'' '+l.Avis+'\n')
            
        else:
            
            cat.write('__label__negatif'' '+l.Avis+'\n')
            
            
            
            
           
def model_fasttext():
   
    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/database.csv')
    
    df = df[df['Sentiment'] != 'Neutre'] # ne garder que le positif ou négatif
    
    #df['Sentiment'] = df['Sentiment'].map({'Positif':1, 'Négatif':0})
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':'positif', 'Négatif':'negatif'})
    
    X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)
   
    # Resampling
    ros = RandomOverSampler(random_state=0)
    
    X_train_re, y_train_re = ros.fit_resample(X_train, y_train)
   
    df_train_resampled = pd.DataFrame()
    
    df_train_resampled["Avis"] = X_train_re
    
    df_train_resampled["Sentiment"] = y_train_re
   
    df_test = pd.DataFrame()
    
    df_test["Avis"] = X_test
    
    df_test["Sentiment"] = y_test
   
    # Version CSV des df_train et df_test  
    df_test.to_csv("test_file.csv")
    
    df_train_resampled.to_csv("train_file_resampled.csv")

    df_train_resampled["Avis"] = df_train_resampled["Avis"].apply(clean_str)
    
    df_test["Avis" ]= df_test["Avis"].apply(clean_str)    
   
    # Entraînement du modèle de classification avec FastText
   
    # Il est nécessaire de transformer df_train en fichier texte :
    to_text(df_train_resampled,"train_file_resampled")
   
    model = fasttext.train_supervised(input="train_file_resampled.txt",
                                      epoch=20,
                                      loss='softmax',
                                      wordNgrams=2,
                                      dim=300,
                                      thread=2,
                                      verbose=2)

    # Sauvegarde du modèle dans un fichier bin
    model.save_model("model_fastttext_resampled.bin")
   
    # Prédictions avec le modèle entraîné
    pred = []
    
    for index,avis_sentiment in df_test.iterrows() :
        
        pred.append(model.predict(avis_sentiment.Avis)[0])

    df_test["Prédictions"] = pred
    
    df_test["Prédictions"] = df_test["Prédictions"].map({('__label__negatif',) : 0, ('__label__positif',) : 1})
    
    df_test["Sentiment"] = df_test["Sentiment"].map({'positif' : 1, 'negatif' : 0})
   
    # Matrice de confusion
    matrice_confusion = confusion_matrix(df_test.Sentiment, df_test.Prédictions)
    
    plt.figure(figsize = (10,7))
    
    sn.heatmap(matrice_confusion, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})
    
    plt.savefig('matrice_confusion_fasttext_resampled', dpi = 400)
   
    # Courbe ROC

    fper, tper, thresholds = roc_curve(df_test["Sentiment"],df_test["Prédictions"])
   
    fig, ax = plt.subplots(figsize=(14,8))
    
    sn.lineplot([0,1], [0,1], ax=ax, color="darkslategray")
    
    sn.lineplot(fper, tper, ax=ax, color="mediumvioletred")
    
    sn.set_style('darkgrid')
    
    ax.set_xlabel( "Taux de faux positifs" , size = 15 )
    
    ax.set_ylabel( "Taux de vrais positifs" , size = 15 )
    
    plt.savefig('Courbe_ROC_fastText', dpi = 400)
   
    return(matrice_confusion)

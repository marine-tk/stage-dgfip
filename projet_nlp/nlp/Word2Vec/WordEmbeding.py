#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 19:44:28 2022

@author: geoffroyperonne
"""

## Importation des librairies


import pandas as pd

import numpy

import string

from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer

from nltk.corpus import stopwords

from gensim.models import keyedvectors



def preprocessing():

    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')

    corpus = df['Avis'].tolist()

    corpus = [avis.lower() for avis in corpus]

    ponctuations = list(string.punctuation)

    corpus = ["".join([char for char in list(avis) if not (char in ponctuations)]) for avis in corpus]

    corpus_tk = [word_tokenize(avis) for avis in corpus]

    lem = WordNetLemmatizer()

    corpus_lm = [[lem.lemmatize(mot) for mot in avis] for avis in corpus_tk]

    mots_vides = stopwords.words("french")

    corpus_sw = [[mot for mot in avis if not (mot in mots_vides)] for avis in corpus_lm]

    trained = keyedvectors.load_word2vec_format('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/frwiki_20180420_300d.txt.bz2', binary=False)

    return(trained,corpus_sw)



def avis2vec(avis, trained, corpus):
    
    p = trained.vectors.shape[1]
    
    vec = numpy.zeros(p)
    
    nb = 0
    
    for tk in avis:
        
        try:
            
            values = trained[tk]
            
            vec += values
            
            nb += 1
        
        except:
            
            pass
        
    if (nb >0):
        
        vec = vec/nb
    
    return(vec)


def corpus2vec():
    
    df_init = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')

    trained, corpus = preprocessing()
    
    print('Préprocessing terminé !')
    
    avisVec = list()
    
    progression = 1
    
    for avis in corpus:
        
        print('Chargement:',progression,'/',len(corpus))
        
        progression += 1
        
        vec = avis2vec(avis, trained, corpus)
        
        avisVec.append(vec)
    
    matVec = numpy.array(avisVec)
    
    df = pd.DataFrame(matVec,columns=['v'+str(i+1) for i in range(matVec.shape[1])])   
    
    df['Sentiment'] = df_init.Sentiment
    
    return(df)
    

    


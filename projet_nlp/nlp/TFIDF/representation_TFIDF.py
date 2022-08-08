#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:37:19 2022

@author: geoffroyperonne
"""

## Importation des librairies

import pandas as pd 

import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from sklearn.pipeline import make_pipeline

from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import MultinomialNB

from sklearn.ensemble import GradientBoostingClassifier

from sklearn.model_selection import GridSearchCV

from sklearn.metrics import confusion_matrix, classification_report, roc_curve

from imblearn.over_sampling import SMOTE

import joblib

import matplotlib.pyplot as plt

import seaborn as sn


## Modèle Random Forest

def modele_random_forest():
    
    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)

    ## CountVectorizer() transforme notre corpus de textes en matrice.
    ## Chaque colonne représente un mot présent dans le corpus.
    ## Chaque ligne représente un texte dans le corpus 
    ## Le coefficient a(i,j) représente le nombre de fois où le mot j est present dans le texte i.
    
    ## TfidfTransformer() transforme la matrice CountVectorizer() en matrice TFIDF.
    ## Le coefficient a(i,j) représente l'importance du mot j dans le texte i.
    ## Cf formule sur internet.
    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    
    ## ???
    pipe.fit(X_train['Avis'])
    
    ## Transforme nos données textuelles en matrice TFIDF.
    feat_train = pipe.transform(X_train['Avis'])
    
    feat_test = pipe.transform(X_test['Avis'])
    
    ## Importation du modèle
    clf = RandomForestClassifier(class_weight={0 : 1 , 1 : 3},
                       max_depth=300,
                       min_samples_split=4,
                       n_estimators=50)
    
    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    feat_train, y_train = sm.fit_resample(feat_train, y_train)
    
    ## Entraine notre modèle
    clf.fit(feat_train, y_train)
    
    y_pred = clf.predict(feat_test)
    
    matrice_confusion = confusion_matrix(y_test, y_pred)
    
    
    return(matrice_confusion,clf.score(feat_test, y_test),y_test,y_pred)



## Modèle Régression Logistique

def modele_logistic_regression():
    
    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)

    ## CountVectorizer() transforme notre corpus de textes en matrice.
    ## Chaque colonne représente un mot présent dans le corpus.
    ## Chaque ligne représente un texte dans le corpus 
    ## Le coefficient a(i,j) représente le nombre de fois où le mot j est present dans le texte i.
    
    ## TfidfTransformer() transforme la matrice CountVectorizer() en matrice TFIDF.
    ## Le coefficient a(i,j) représente l'importance du mot j dans le texte i.
    ## Cf formule sur internet.
    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    
    ## ???
    pipe.fit(X_train['Avis'])
    
    ## Transforme nos données textuelles en matrice TFIDF.
    feat_train = pipe.transform(X_train['Avis'])
    
    feat_test = pipe.transform(X_test['Avis'])
    
    ## Importation du modèle
    clf = LogisticRegression(penalty = 'l2', dual = False, C = 10, 
                             class_weight = None, max_iter = 100, solver='newton-cg')

    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    feat_train, y_train = sm.fit_resample(feat_train, y_train)
    
    ## Entraine notre modèle
    clf.fit(feat_train, y_train)
    
    y_pred = clf.predict(feat_test)
    
    matrice_confusion = confusion_matrix(y_test, y_pred)
    
    joblib.dump(clf,'modele_RL_TFIDF.pkl')
    
    return(matrice_confusion,clf.score(feat_test, y_test),y_test,y_pred)



## Modèle Bayes Naif

def modele_bayes():
    
    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)

    ## CountVectorizer() transforme notre corpus de textes en matrice.
    ## Chaque colonne représente un mot présent dans le corpus.
    ## Chaque ligne représente un texte dans le corpus 
    ## Le coefficient a(i,j) représente le nombre de fois où le mot j est present dans le texte i.
    
    ## TfidfTransformer() transforme la matrice CountVectorizer() en matrice TFIDF.
    ## Le coefficient a(i,j) représente l'importance du mot j dans le texte i.
    ## Cf formule sur internet.
    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    
    ## ???
    pipe.fit(X_train['Avis'])
    
    ## Transforme nos données textuelles en matrice TFIDF.
    feat_train = pipe.transform(X_train['Avis'])
    
    feat_test = pipe.transform(X_test['Avis'])
    
    ## Importation du modèle
    clf = MultinomialNB(alpha = 2 , fit_prior = True , class_prior = np.array([0.35, 0.65]))

    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    feat_train, y_train = sm.fit_resample(feat_train, y_train)
    
    ## Entraine notre modèle
    clf.fit(feat_train, y_train)
    
    y_pred = clf.predict(feat_test)
    
    matrice_confusion = confusion_matrix(y_test, y_pred)
    
    
    return(matrice_confusion,clf.score(feat_test, y_test),y_test,y_pred)


## Modèle Gradient Boosting

def modele_gradient_boosting():
    
    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)

    ## CountVectorizer() transforme notre corpus de textes en matrice.
    ## Chaque colonne représente un mot présent dans le corpus.
    ## Chaque ligne représente un texte dans le corpus 
    ## Le coefficient a(i,j) représente le nombre de fois où le mot j est present dans le texte i.
    
    ## TfidfTransformer() transforme la matrice CountVectorizer() en matrice TFIDF.
    ## Le coefficient a(i,j) représente l'importance du mot j dans le texte i.
    ## Cf formule sur internet.
    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    
    ## ???
    pipe.fit(X_train['Avis'])
    
    ## Transforme nos données textuelles en matrice TFIDF.
    feat_train = pipe.transform(X_train['Avis'])
    
    feat_test = pipe.transform(X_test['Avis'])
    
    ## Importation du modèle
    clf = GradientBoostingClassifier(n_estimators=150, max_depth=10, min_samples_split=4)

    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    feat_train, y_train = sm.fit_resample(feat_train, y_train)
    
    ## Entraine notre modèle
    clf.fit(feat_train, y_train)
    
    y_pred = clf.predict(feat_test)
    
    matrice_confusion = confusion_matrix(y_test, y_pred)
    
    
    return(matrice_confusion,clf.score(feat_test, y_test),y_test,y_pred)


## Visualisation

    
def representation(modele):
    
    if modele == 'tree':
        
        matrice , score , y_test , y_pred = modele_random_forest()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_tree', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
    
    if modele == 'regression logistique':
        
        matrice , score , y_test , y_pred = modele_logistic_regression()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_logit_reg', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
    if modele == 'bayes':
        
        matrice , score , y_test , y_pred = modele_bayes()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_bayes', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
    if modele == 'gradient':
        
        matrice , score , y_test , y_pred = modele_gradient_boosting()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_gradient_boosting', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
    
    
def best_parameters(name_model) :

    if name_model == 'regression logistique' :
        
        df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/Données/Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)

        model = LogisticRegression()

        parameter_space = {'max_iter': [100,500,1000],
                           'class_weight' : [None, 'balanced'],
                           'C' : [0.001,0.01,0.1,1,10,100],
                           'penalty' : ['l1', 'l2', 'elasticnet'],
                           'solver' : ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']
                            }
            
        CV=3

        clf = GridSearchCV(model, parameter_space, cv=CV,verbose=3,scoring='f1_macro')
        
        clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

        print('Best parameters found:', clf.best_params_)


    if name_model == 'tree' :
        
        df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/Données/Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)

        model = RandomForestClassifier(class_weight = {0 : 1 , 1 : 1.3},criterion = 'gini')

        parameter_space = parameter_space = {'n_estimators': [10,50,100],
                                                 'max_depth' : [10,100,300],
                                                 'min_samples_split': [2, 4]}

        CV=3

        clf = GridSearchCV(model, parameter_space, cv=CV,verbose=3,scoring='f1_macro')
        
        clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

        print('Best parameters found:', clf.best_params_)

    if name_model == 'bayes' :
        
        df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/Données/Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)

        model = MultinomialNB(alpha = 1 , fit_prior = True , class_prior = np.array([0.2, 0.8]))

        parameter_space = parameter_space = {'alpha': [0.025,0.05,0.1],
                                                 'fit_prior' : [False,True]}

        CV=3

        clf = GridSearchCV(model, parameter_space, cv=CV,verbose=3,scoring='f1_macro')
        
        clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

        print('Best parameters found:', clf.best_params_)


    if name_model == 'gradient' :
        
        df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/Données/Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
        
        model = GradientBoostingClassifier(n_estimators=200, max_depth=40)

        parameter_space = parameter_space = {'n_estimators': [10,50,100],
                                             'max_depth' : [10,20,40],
                                             'min_samples_split': [2, 4]}

        CV=3

        clf = GridSearchCV(model, parameter_space, cv=CV,verbose=3,scoring='f1_macro')
        
        clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

        print('Best parameters found:', clf.best_params_)
        
        
        
        
def plot_roc_curve(fper_rf, tper_rf, fper_rl, tper_rl, fper_bn, tper_bn, fper_gb, tper_gb):
    
    fig, ax = plt.subplots(figsize=(14,8))
    
    sn.lineplot([0,1], [0,1], ax=ax, color="darkslategray")
    
    sn.lineplot(fper_rf, tper_rf, ax=ax, color="darkcyan")
    
    sn.lineplot(fper_rl, tper_rl, ax=ax)
    
    sn.lineplot(fper_bn, tper_bn, ax=ax, color="darkmagenta")
    
    sn.lineplot(fper_gb, tper_gb, ax=ax, color="seagreen")
    
    ax.set_xlabel( "Taux de faux positifs" , size = 15 ) 
    
    ax.set_ylabel( "Taux de vrais positifs" , size = 15 ) 
    
    ax.legend(['Classifieur aléatoire','Random Forest','Régression Logistique','Bayes naïf','Gradient Boosting'], facecolor='w')
    
    sn.set_style('darkgrid')
    
    plt.savefig('Courbe_ROC', dpi = 400)
    



def roc_curves():
    
    ## Random Forest

    matrice , score , y_test , y_pred = modele_random_forest()
    
    fper_rf, tper_rf, thresholds = roc_curve(y_test, y_pred)
    
    ## Regression Logistique
    
    matrice , score , y_test , y_pred = modele_logistic_regression()
    
    fper_rl, tper_rl, thresholds = roc_curve(y_test, y_pred)    

    ## Bayes naïf
    
    matrice , score , y_test , y_pred = modele_bayes()
    
    fper_bn, tper_bn, thresholds = roc_curve(y_test, y_pred)  
    
    ## Gradient Boosting
    
    matrice , score , y_test , y_pred = modele_gradient_boosting()
    
    fper_gb, tper_gb, thresholds = roc_curve(y_test, y_pred)  
    
    
    plot_roc_curve(fper_rf, tper_rf, fper_rl, tper_rl, fper_bn, tper_bn, fper_gb, tper_gb) 
    
        

        
        
        
        
        
        
        
        
        
        

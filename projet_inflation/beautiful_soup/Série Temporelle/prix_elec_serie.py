#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 23:07:30 2022

@author: geoffroyperonne
"""

## Importation des librairies 

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

import datetime

import itertools

import statsmodels

import statsmodels.api as sm

from statsmodels.tsa.seasonal import seasonal_decompose

from pmdarima import model_selection

from statsmodels.tsa.stattools import adfuller

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from pandas.plotting import register_matplotlib_converters

import warnings; warnings.filterwarnings(action='once')

register_matplotlib_converters()

from pmdarima import auto_arima

from pylab import rcParams

from cycler import cycler
  
import warnings

warnings.filterwarnings("ignore")




## Création du DataFrame de travail

def importation():
    
    df_init = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet inflation/Série Temporelle/evolution-des-prix-domestiques-du-gaz-et-de-lelectricite.csv', sep = ';')
    
    df = pd.DataFrame({'Année': df_init['Année'].tolist(),
                       
                       'Semestre': df_init['Semestre'].tolist(),
                       
                       'Date': [0 for i in range(len(df_init))],
                       
                       'Prix': df_init['France –  Electricité'].tolist()})
    
    df = df.sort_values(by=['Année'])
    
    df = df.iloc[20:]

    
    return(df)


def formatage():
    
    df = importation()
    
    df = df.reset_index()
    
    del df['index']
    
    for i in range(len(df)):
        
        if df['Semestre'][i] == 'S1':
            
            df['Date'][i] = datetime.datetime(df['Année'][i],1,1,0,0,0)
            
        if df['Semestre'][i] == 'S2':
            
            df['Date'][i] = datetime.datetime(df['Année'][i],6,1,0,0,0)
            
    df.sort_index(axis = 0, ascending = False)
        
    del df['Année']
    
    del df['Semestre']
    
    df = df.sort_values(by=['Date'])
    
    df = df.drop(df[df.index.duplicated()].index.tolist())
    
    df = df.reset_index()
    
    df.set_index('Date', inplace = True)
    
    del df['index']
    
    df=df.asfreq('6M', method='ffill')
    
    return(df)
    
    


## Visualisation de la consommation d'électricité

def visualisation_brute():
    
    sns.set_style('darkgrid')
    
    fig, ax = plt.subplots(figsize=(25,8))
    
    df = formatage()
    
    df['Date'] = df.index
    
    sns.lineplot(df['Date'].tolist(), df['Prix'].tolist(), ax=ax, color="darkcyan")
    
    plt.savefig('Serie_temp_brute_prix', dpi = 400)
    
    return(df)
 
    
## Décomposition de la série
    
def decomposition():
    
    rcParams['axes.prop_cycle'] =  cycler(color =["darkcyan"])
    
    df = formatage()

    df = df.dropna() 
    
    #df = df.iloc[3200:]
    
    #for i in range(len(dl)):
        
        #if pd.isnull(dl.iloc[i,0]):
            
            #dl.iloc[i,0] = dl.iloc[i-1,0]
    
    result = seasonal_decompose(df, 
                            model ='additive')
  
    result.plot()
    
    plt.savefig('Serie_temp_decomposition_prix_elec', dpi = 400)
    

## Stationarisation de la série

def statio():
    
    df = formatage()
    
    df = df.apply(np.log)
    
    df = df.diff(1)
    
    return(df)
    
    
    
## Visualisation ACF & PACF

def p_acf():
    
    large = 22; med = 16
    
    params = {'axes.titlesize': large,
              
              'legend.fontsize': med,
              
              'figure.figsize': (20, 10),
              
              'axes.labelsize': med,
              
              'xtick.labelsize': med,
              
              'ytick.labelsize': med,
              
              'figure.titlesize': large}
    
    plt.rcParams.update(params)
    
    plt.style.use('seaborn-whitegrid')
    
    sns.set_style('darkgrid') #'white'


    df = formatage()


    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(16,6), dpi= 80)
    plot_acf(df.Prix.tolist(), ax=ax1, lags=27)
    plot_pacf(df.Prix.tolist(), ax=ax2, lags=10)


    ax1.spines["top"].set_alpha(.3); ax2.spines["top"].set_alpha(.3)
    ax1.spines["bottom"].set_alpha(.3); ax2.spines["bottom"].set_alpha(.3)
    ax1.spines["right"].set_alpha(.3); ax2.spines["right"].set_alpha(.3)
    ax1.spines["left"].set_alpha(.3); ax2.spines["left"].set_alpha(.3)


    ax1.tick_params(axis='both', labelsize=12)
    ax2.tick_params(axis='both', labelsize=12)
    #plt.show()
    
    plt.savefig('ACF_PACF_prix_elec', dpi = 400)    
    
    
## Vérification de la stationarité 
    
def get_stationarity():
    
    df = statio()
    
    df = df.iloc[1:]
    
    df['Date'] = df.index
    
    
    
    # Statistiques mobiles
    rolling_mean = df['Prix'].rolling(window=4).mean()
    
    rolling_std = df['Prix'].rolling(window=4).std()
    
    
    
    # tracé statistiques mobiles
    
    sns.set_style('darkgrid')
    
    fig, ax = plt.subplots(figsize=(25,8))
    
    sns.lineplot(df['Date'].tolist(), df['Prix'].tolist(), color="darkcyan", label='Origine')
    
    sns.lineplot(df['Date'].tolist(), rolling_mean, color="darkmagenta", label='Moyenne Mobile')
    
    sns.lineplot(df['Date'].tolist(), rolling_std, color='seagreen', label='Ecart-type Mobile')
    
    plt.savefig('Serie_temp_moyenne_et_mobile', dpi = 400)
    
    
    
    # Test Dickey–Fuller :
    result = adfuller(df['Prix'])
    
    print('Statistiques ADF : {}'.format(result[0]))
    
    print('p-value : {}'.format(result[1]))
    
    print('Valeurs Critiques :')
    
    for key, value in result[4].items():
        
        print('\t{}: {}'.format(key, value))
        
        
        
        
        
        









def modele():
    
    df = formatage()
    
    # Construction du modèle
    arima = statsmodels.tsa.arima.model.ARIMA(df, order=(3, 0, 1), enforce_stationarity=False, enforce_invertibility=False, trend_offset=1, freq='6M')
                                    
    # Fit du modèle
    output = arima.fit()
    
    return(output)



def sommaire():
    
    output = modele()
    
    # Résumé du modèle
    print(output.summary())
    
    
    
def diagnostique():
    
    output = modele()

    # Affichage du diagnostique 
    output.plot_diagnostics(figsize=(16,10))
    
    plt.savefig('Diagnistique_prix_elec', dpi = 400)

    
    
    
def prediction():
    
    df = formatage()
    
    output = modele()
    
    pred = output.get_prediction(start=pd.to_datetime('2014-07-31 00:00:00'), dynamic=False)

    pred_ci = pred.conf_int()
    
    #rcParams['axes.prop_cycle'] =  cycler(color =["darkmagenta"])
    
    sns.set_style('darkgrid')

    ax = df.plot(label='Observation', color = 'teal')

    pred.predicted_mean.plot(ax=ax, label='Prédiction', alpha=.7, figsize=(14, 4), color = 'darkmagenta')

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='orchid', alpha=.2)

    ax.set_xlabel('Date')

    ax.set_ylabel('Consommation (MW)')

    plt.legend()

    plt.savefig('Comparaison_observation_prediction_prix_elec', dpi = 400)
    
    

def future():
    
    df = formatage()
    
    output = modele()
    
    pred_uc = output.get_forecast(steps=30)

    pred_ci = pred_uc.conf_int()

    ax = df.plot(label='Observation', figsize=(14, 4), color = 'teal')

    pred_uc.predicted_mean.plot(ax=ax, label='Prédiction', color = 'darkmagenta')

    ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='orchid', alpha=.25)

    ax.set_xlabel('Date')

    ax.set_ylabel('Prix')

    plt.legend()

    plt.savefig('prediction_prix_elec', dpi = 400)
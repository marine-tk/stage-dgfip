#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 14:04:04 2022

@author: geoffroyperonne
"""

## Importation des librairies 

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

import datetime

import itertools

import statsmodels.api as sm

from statsmodels.tsa.seasonal import seasonal_decompose

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
    
    df_init = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet inflation/Série Temporelle/consommation-quotidienne-brute-2.csv', sep = ';')
    
    df = pd.DataFrame({'Date + Heure': df_init['Date - Heure'].tolist(),
                       
                       'Date': [0 for i in range(len(df_init))],
                       
                       'Consommation': df_init['Consommation brute électricité (MW) - RTE'].tolist()})
    
    return(df)


def formatage():
    
    df = importation()
    
    for i in range(len(df)):
        
        df['Date'][i] = datetime.datetime(int(df['Date + Heure'][i][:4]), 
                                          int(df['Date + Heure'][i][5:7]), 
                                          int(df['Date + Heure'][i][8:10]),
                                          int(df['Date + Heure'][i][11:13]),
                                          int(df['Date + Heure'][i][14:16]), 0)
        
    del df['Date + Heure']
    
    df.set_index('Date', inplace = True)
    
    df = df.drop(df[df.index.duplicated()].index.tolist())
    
    df=df.asfreq('W', method='ffill')
    
    return(df)
    
    


## Visualisation de la consommation d'électricité

def visualisation_brute():
    
    sns.set_style('darkgrid')
    
    fig, ax = plt.subplots(figsize=(25,8))
    
    df = formatage()
    
    df['Date'] = df.index
    
    sns.lineplot(df['Date'].tolist(), df['Consommation'].tolist(), ax=ax, color="darkcyan")
    
    plt.savefig('Serie_temp_brute', dpi = 400)
    
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
    
    plt.savefig('Serie_temp_decomposition', dpi = 400)
    
    
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
    plot_acf(df.Consommation.tolist(), ax=ax1, lags=70)
    plot_pacf(df.Consommation.tolist(), ax=ax2, lags=30)


    ax1.spines["top"].set_alpha(.3); ax2.spines["top"].set_alpha(.3)
    ax1.spines["bottom"].set_alpha(.3); ax2.spines["bottom"].set_alpha(.3)
    ax1.spines["right"].set_alpha(.3); ax2.spines["right"].set_alpha(.3)
    ax1.spines["left"].set_alpha(.3); ax2.spines["left"].set_alpha(.3)


    ax1.tick_params(axis='both', labelsize=12)
    ax2.tick_params(axis='both', labelsize=12)
    #plt.show()
    
    plt.savefig('ACF_PACF', dpi = 400)    
    
    
## Vérification de la stationarité 
    
def get_stationarity():
    
    df = formatage()
    
    df['Date'] = df.index
    
    
    
    # Statistiques mobiles
    rolling_mean = df['Consommation'].rolling(window=4).mean()
    
    rolling_std = df['Consommation'].rolling(window=4).std()
    
    
    
    # tracé statistiques mobiles
    
    sns.set_style('darkgrid')
    
    fig, ax = plt.subplots(figsize=(25,8))
    
    sns.lineplot(df['Date'][:3000].tolist(), df['Consommation'][:3000].tolist(), color="darkcyan", label='Origine')
    
    sns.lineplot(df['Date'][:3000].tolist(), rolling_mean[:3000], color="darkmagenta", label='Moyenne Mobile')
    
    sns.lineplot(df['Date'][:3000].tolist(), rolling_std[:3000], color='seagreen', label='Ecart-type Mobile')
    
    plt.savefig('Serie_temp_moyenne_et_mobile', dpi = 400)
    
    
    
    # Test Dickey–Fuller :
    result = adfuller(df['Consommation'])
    
    print('Statistiques ADF : {}'.format(result[0]))
    
    print('p-value : {}'.format(result[1]))
    
    print('Valeurs Critiques :')
    
    for key, value in result[4].items():
        
        print('\t{}: {}'.format(key, value))
        
        
        
def sarima_forecast():
    
    df = formatage()
    
    p = d = q = range(1, 3)

    pdq = list(itertools.product(p, d, q))

    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    
    ans = []
    
    for param in pdq:
        
        for param_seasonal in seasonal_pdq:
        
            try:
            
                mod = sm.tsa.statespace.SARIMAX(df,order=param,seasonal_order=param_seasonal,enforce_stationarity=False,enforce_invertibility=False)
            
                results = mod.fit()
                
                ans.append([param,param_seasonal,results.aic])
            
            except: 
            
                continue
            
            
    ans_df = pd.DataFrame(ans, columns=['pdq', 'pdqs', 'aic'])
    
    ans_df = ans_df.sort_values(by=['aic'],ascending=True)[0:5]
    
    return(ans_df)



def modele():
    
    df = formatage()
    
    # Construction du modèle
    sarimax = sm.tsa.statespace.SARIMAX(df, 
                                    order=(2,0,8), 
                                    seasonal_order=(8,0,8,52), 
                                    enforce_stationarity=False, 
                                    enforce_invertibility=False,
                                    freq='W')
                                    
    # Fit du modèle
    output = sarimax.fit()
    
    return(output)



def sommaire():
    
    output = modele()
    
    # Résumé du modèle
    print(output.summary())
    
    
    
def diagnostique():
    
    output = modele()

    # Affichage du diagnostique 
    output.plot_diagnostics(figsize=(16,10))
    
    plt.savefig('Diagnostique', dpi = 400)

    
    
    
def prediction():
    
    df = formatage()
    
    output = modele()
    
    pred = output.get_prediction(start=pd.to_datetime('2020-01-05 00:00:00'), dynamic=False)

    pred_ci = pred.conf_int()
    
    #rcParams['axes.prop_cycle'] =  cycler(color =["darkmagenta"])
    
    sns.set_style('darkgrid')

    ax = df[300:].plot(label='Observation', color = 'teal')

    pred.predicted_mean.plot(ax=ax, label='Prédiction', alpha=.7, figsize=(14, 4), color = 'darkmagenta')

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='orchid', alpha=.2)

    ax.set_xlabel('Date')

    ax.set_ylabel('Consommation (MW)')

    plt.legend()

    plt.savefig('Comparaison_observation_prediction', dpi = 400)
    
    

def future():
    
    df = formatage()
    
    output = modele()
    
    pred_uc = output.get_forecast(steps=100)

    pred_ci = pred_uc.conf_int()

    ax = df[300:].plot(label='Observation', figsize=(14, 4), color = 'teal')

    pred_uc.predicted_mean.plot(ax=ax, label='Prédiction', color = 'darkmagenta')

    ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='orchid', alpha=.25)

    ax.set_xlabel('Date')

    ax.set_ylabel('Consommation (MW)')
    
    plt.ylim(20000,100000)

    plt.legend()

    plt.savefig('prediction_conso', dpi = 400)
    
    return(output)





            


        
        
        
        
        
        
        
        
        

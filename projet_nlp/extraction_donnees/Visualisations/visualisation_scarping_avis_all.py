#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:25:29 2022

@author: geoffroyperonne
"""

## Importation des librairies

import seaborn as sns

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

from PIL import Image

from stop_words import get_stop_words

from wordcloud import WordCloud




## Statistiques descriptives

def stat_des():

    df = pd.read_csv("/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv")
    
    df = df[df['Sentiment'] != 'Neutre']
    
    sns.histplot(data = df['Sentiment'] , shrink = 0.8 , color="darkcyan" , stat = 'percent' )
    
    sns.set_style('darkgrid')
    
    plt.savefig('pourcentage_sentiment', dpi = 400)
    
    
## Wordcloud

def word_cloud():
    
    stopwords = get_stop_words('fr')
    
    stopwords1 = set(["faut","peux","puis","n'a","n'y","n'est","j'avais","qu'il","d'une","d'un","pu","s'est","n'ai","m'a","c'est","j'ai","ai","avais","a","as","avons","est","etait","ete","la","j","d","l",
                      "peu","en","ce","au","vu","faire","pour","une","nan","de","et","nous","que","si","le","il","ma","vous","y","c","des","on","un","les","je","ne","pas","ces","m","qu","fallut","ou","sur","du","fais","me","fait","fur","mais","cela","pr","avait","mis","plus","tous","part","sinon","tout","sont","sans","an","qui","cest","cas","par","memes","meme",
                      "sous","aurais","malgre","etaient","vraiment","donc","votre","plutot","passe",
                      "n","avoir","aussi","chose","assez","trop","moins","mieux","beaucoup","grace","cette","vrai","voir","choses","trouve","journee","appris","pense","bien","bonjour"])
    
    stopwords = set(stopwords)|set(stopwords1)
    
    df = pd.read_csv("/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/Extraction tweets/Bases de données/scrapping_avis_all.csv")
    
    mask = np.array(Image.open("cloud.PNG"))
    
    mask[mask == 1] = 255
    
    ## Pour les commentaires positifs
    df_positif=df[df['Sentiment']=='Positif']
    
    positif = ""
    
    for i in range(len(df_positif)):
        
        positif += df_positif.iloc[i][1].lower()
        
    wordcloud = WordCloud(max_words=150, stopwords=stopwords, background_color='white', width = 1920 , height = 1080 , colormap = "Greens" , mask = mask).generate(positif)
    
    plt.imshow(wordcloud)
    
    plt.axis('off')
    
    plt.savefig('wourdcloud_positif', dpi = 400)
    
    
    ## Pour les commentaires negatifs
    df_negatif=df[df['Sentiment']=='Négatif']
    
    negatif = ""
    
    for i in range(len(df_negatif)):
        
        negatif += df_negatif.iloc[i][1].lower()
        
    wordcloud = WordCloud(max_words=150, stopwords=stopwords, background_color='white', width = 1920 , height = 1080 , colormap = "BuPu" , mask = mask).generate(negatif)
    
    plt.imshow(wordcloud)
    
    plt.axis('off')
    
    plt.savefig('wourdcloud_negatif', dpi = 400)



    

    
    

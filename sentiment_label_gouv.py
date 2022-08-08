#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:12:12 2022

@author: geoffroyperonne
"""

## Importation des librairies

from bs4 import BeautifulSoup

import requests

import pandas as pd

## Scraping des avis

def clean_sentiment(str) :

    ## permet de supprimer les espaces et les sauts de lignes des avis 
    
    str = str.replace(' ','')
    
    str = str.replace('\n','')
    
    return str

def scrapping_avis_all() :

    ## On créer un DataFrame vide qui contiendra nos avis et nos labels 
    
    df = pd.DataFrame(columns=["Avis","Sentiment"])

    ## On récupère ces données sur un site du gouvernement
    
    base = 'https://www.plus.transformation.gouv.fr'

    ## experience est une liste contenant l'ensemble des url des avis 
    
    experiences = []

    # On mettra ces listes dans le dataframe

    avis = []
    
    sentiment = []

    page_progress = 0

    ## On parcourt l'ensemble des pages web des avis. Il y en a 823 à l'heure où ce code est rédigé
    
    for num_page in range(823) :
        
        page_progress+=1
        
        url = 'https://www.plus.transformation.gouv.fr/experiences?combine=&reponse=All&organisme=&page='
        
        req = requests.get(url+str(num_page), headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}).text
        
        soup = BeautifulSoup(req, "html.parser")
        
        card_link = soup.findAll(class_='fr-card__link',href=True)

        # On met dans une liste toutes les fins d'URL des expériences qu'on va parcourir

        for link in card_link :
            
            experiences.append(link['href'])
       
        print("Page "+str(page_progress)+" sur "+"823")
   
    exp_progress = 0

    ## On parcourt l'ensemble des avis 
    
    for exp in experiences :
        
        exp_progress+=1
        
        url = base+exp
        
        req = requests.get(url , headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}).text
        
        soup = BeautifulSoup(req, "html.parser")
       
        # Avis utilisateur
        avis.append(soup.find("article").find("div").text)

        # Sentiment attribué
        sentiment.append(clean_sentiment(soup.find("div",{'class' : "experience-feeling-status fr-text--lg fr-text--bold fr-mb-4w"}).text))

        print("Progression : "+str(exp_progress)+"/"+str(len(experiences)))
       
        
    df["Avis"] = avis
    
    df["Sentiment"] = sentiment

    ## On enregistre la base de données créee.
   
    df.to_excel('scrapping_avis_all.xlsx')
    
    df.to_csv('scrapping_avis_all.csv')  


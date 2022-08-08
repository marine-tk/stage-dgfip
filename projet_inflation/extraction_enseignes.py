#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:28:43 2022

@author: geoffroyperonne
"""

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

import pandas as pd

from datetime import datetime

import time



def clean_price(str):
    
    str = str.replace(' ','')
    
    str = str.replace('\n','')
    
    str = str.replace('€/L','')
    
    str = str.replace('€/U','')
    
    str = str.replace(',','.')
    
    str = str.replace('/','')
    
    str = str.replace('kg','')
    
    str = str.replace('KG','')
    
    str = str.replace('€/KG','')
    
    str = str.replace('€','')
    
    return(float(str))


def clean_article(str):
    
    str = str.replace(' ','_')
    
    str = str.lower()
    
    return(str)

def clean_quantite(str):
    
    liste = str.split()
    
    for i in range(len(liste)):
        
        if liste[i][0] == '(':
            
            result = liste[i] + ' ' + liste[i+1] 
            
            try:
                
                result += ' ' + liste[i+2]
                
            except:
                
                pass
            
    return(result)


def separateur(str):
    
    liste = str.split()
    
    for i in range(len(liste)):
        
        if liste[i][-1] == ',':
            
            ori = liste[i+1:]

            art = liste[:i+1]
            
    origine, article = '', ''
    
    for i in range(len(art)):
        
        article += art[i] + ' '
        
    for i in range(len(ori)):
        
        origine += ori[i] + ' '
    
    return(article, origine)




## Fruits


def extraction_fruit():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_fruit_carrefour = [
                     'https://www.carrefour.fr/p/kiwi-bio-jaune-sungold-3523680428430?t=1883',
                     'https://www.carrefour.fr/p/abricots-du-languedoc-reflets-de-france-3276555385726?t=1883',
                     'https://www.carrefour.fr/p/abricots-moyens-vrac-3276552267216?t=1883',
                     'https://www.carrefour.fr/p/ananas-extra-sweet-3000001033257?t=1883',
                     'https://www.carrefour.fr/p/raisin-bio-blanc-italia-3270190218579?t=1883',
                     'https://www.carrefour.fr/p/citrons-bio-3270190010272?t=1883',
                     'https://www.carrefour.fr/p/prunes-rouges-flavorking-vrac-3000000035672?t=1883',
                     'https://www.carrefour.fr/p/peches-chair-jaune-vrac-filiere-qualite-carrefour-3276550205982?t=1883',
                     'https://www.carrefour.fr/p/melon-galia-3000001033776?t=1883',
                     'https://www.carrefour.fr/p/melon-blanc-3276558894027?t=1883',
                     'https://www.carrefour.fr/p/framboise-cee-3276555792975?t=1883',
                     'https://www.carrefour.fr/p/framboises-3276554564405?t=1883',
                     'https://www.carrefour.fr/p/cerises-rouges-moyennes-vrac-3276552272555?t=1883',
                     'https://www.carrefour.fr/p/poires-william-vertes-vrac-filiere-qualite-carrefour-3276552250706?t=1883',
                     'https://www.carrefour.fr/p/poires-angelys-vrac-3276555766914?t=1883',
                     'https://www.carrefour.fr/p/raisin-rose-sans-pepin-sable-3276550157908?t=1883',
                     'https://www.carrefour.fr/p/fraises-rondes-3276554567963?t=1883',
                     'https://www.carrefour.fr/p/fraises-gariguette-3276554568076?t=1883',
                     'https://www.carrefour.fr/p/fraises-ciflorette-3523680265578?t=1883',
                     'https://www.carrefour.fr/p/myrtilles-3523680432901?t=1883',
                     'https://www.carrefour.fr/p/bananes-bio-cavendish-3523680294349?t=1883',
                     'https://www.carrefour.fr/p/kiwi-hayward-bio-3276555768321?t=1883',
                     'https://www.carrefour.fr/p/ananas-bio-extra-sweet-carrefour-3523680409248?t=1883',
                     'https://www.carrefour.fr/p/pommes-bicolores-bio-3276550311843?t=1883',
                     'https://www.carrefour.fr/p/oranges-navel-bio-3276557071313?t=1883',
                     'https://www.carrefour.fr/p/pomelos-roses-bio-3276550320333?t=1883',
                     'https://www.carrefour.fr/p/bananes-plantain-jaunes-vrac-3276557654653?t=1883',
                     'https://www.carrefour.fr/p/litchis-vrac-3276554645425?t=1883',
                     'https://www.carrefour.fr/p/grenade-3276554651631?t=1883'
                     ]

    percent_carrefour = 0

    for url in url_fruit_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[2]').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('fruit')
            
            enseigne.append('carrefour')
            
            origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_fruit_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les fruits de Carrefour :',percent_carrefour/len(url_fruit_carrefour)*100,'%')
        
    progression = 0
    
    XPATH_articles = [
        '//*[@id="204"]/div[1]/section/article[2]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[3]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[4]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[7]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[8]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[9]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[10]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[12]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[13]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[15]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[16]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[20]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[21]/a/div[2]/h1',
        '//*[@id="204"]/div[1]/section/article[22]/a/div[2]/h1',
        
        '//*[@id="204"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[3]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[9]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[10]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[13]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[24]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[25]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[29]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[32]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[37]/a/div[2]/h1',
        '//*[@id="204"]/div[2]/section/article[38]/a/div[2]/h1',
        
        '//*[@id="204"]/div[3]/section/article[1]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[2]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[7]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[8]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[15]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[16]/a/div[2]/h1',
        '//*[@id="204"]/div[3]/section/article[20]/a/div[2]/h1',
        
        '//*[@id="204"]/div[5]/section/article[1]/a/div[2]/h1',
        '//*[@id="204"]/div[5]/section/article[2]/a/div[2]/h1',
        '//*[@id="204"]/div[5]/section/article[3]/a/div[2]/h1',
        '//*[@id="204"]/div[5]/section/article[17]/a/div[2]/h1',
        '//*[@id="204"]/div[5]/section/article[19]/a/div[2]/h1',
        '//*[@id="204"]/div[5]/section/article[20]/a/div[2]/h1',
        
        '//*[@id="204"]/div[6]/section/article[19]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[20]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[22]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[25]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[27]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[29]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[30]/a/div[2]/h1',
        '//*[@id="204"]/div[6]/section/article[43]/a/div[2]/h1'
        
        ]
    
    XPATH_prix = [
        '//*[@id="204"]/div[1]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[3]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[4]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[7]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[8]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[9]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[10]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[12]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[13]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[15]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[16]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[20]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[21]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[1]/section/article[22]/a/div[2]/p/span[2]',
        
        '//*[@id="204"]/div[2]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[3]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[9]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[10]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[13]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[24]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[25]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[29]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[32]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[37]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[2]/section/article[38]/a/div[2]/p/span[2]',
        
        '//*[@id="204"]/div[3]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[7]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[8]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[15]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[16]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[3]/section/article[20]/a/div[2]/p/span[2]',
        
        '//*[@id="204"]/div[5]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[5]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[5]/section/article[3]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[5]/section/article[17]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[5]/section/article[19]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[5]/section/article[20]/a/div[2]/p/span[2]',
        
        '//*[@id="204"]/div[6]/section/article[19]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[20]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[22]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[25]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[27]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[29]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[30]/a/div[2]/p/span[2]',
        '//*[@id="204"]/div[6]/section/article[43]/a/div[2]/p/span[2]'
        
        ]
    
    XPATH_quantite = [
            '//*[@id="204"]/div[1]/section/article[2]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[3]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[4]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[7]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[8]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[9]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[10]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[12]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[13]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[15]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[16]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[20]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[21]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[1]/section/article[22]/a/div[2]/p/span[1]',
            
            '//*[@id="204"]/div[2]/section/article[1]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[3]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[9]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[10]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[13]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[24]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[25]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[29]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[32]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[37]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[2]/section/article[38]/a/div[2]/p/span[1]',
            
            '//*[@id="204"]/div[3]/section/article[1]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[2]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[7]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[8]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[15]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[16]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[3]/section/article[20]/a/div[2]/p/span[1]',
            
            '//*[@id="204"]/div[5]/section/article[1]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[5]/section/article[2]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[5]/section/article[3]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[5]/section/article[17]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[5]/section/article[19]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[5]/section/article[20]/a/div[2]/p/span[1]',
            
            '//*[@id="204"]/div[6]/section/article[19]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[20]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[22]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[25]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[27]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[29]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[30]/a/div[2]/p/span[1]',
            '//*[@id="204"]/div[6]/section/article[43]/a/div[2]/p/span[1]'
        

        ]
    
    driver.get('https://www.labellevie.com/categorie/204/fruits')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append(clean_article(pays))
        
            categorie.append('fruit')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,XPATH_quantite[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/204/fruits')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_prix))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les fruits de La Belle Vie :',percent_lbv/len(XPATH_prix)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)



def extraction_legume():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_legume_carrefour = [
                    'https://www.carrefour.fr/p/avocat-hass-bio-3523680432437?t=1892',
                    'https://www.carrefour.fr/p/radis-roses-3276557117929?t=1892',
                    'https://www.carrefour.fr/p/concombre-3000001038733?t=1892',
                    'https://www.carrefour.fr/p/concombre-bio-3276555848665?t=1892',
                    'https://www.carrefour.fr/p/courgettes-vrac-3000000038857?t=1892',
                    'https://www.carrefour.fr/p/tomates-rondes-charnues-a-farcir-vrac-3000000040676?t=1892',
                    'https://www.carrefour.fr/p/tomates-allongees-coeur-vrac-3523680304352?t=1892',
                    'https://www.carrefour.fr/p/tomates-cotelees-jaunes-vrac-3276552413774?t=1892',
                    'https://www.carrefour.fr/p/patates-douces-vrac-3000000041376?t=1892',
                    'https://www.carrefour.fr/p/artichaut-blanc-3276556231909?t=1892',
                    'https://www.carrefour.fr/p/mais-doux-3276554797810?t=1892',
                    'https://www.carrefour.fr/p/mais-doux-3276554797834?t=1892',
                    'https://www.carrefour.fr/p/aubergine-bio-3523680454644?t=1892',
                    'https://www.carrefour.fr/p/concombre-bio-carrefour-bio-3276559349953?t=1892',
                    'https://www.carrefour.fr/p/betteraves-bio-3281440000028?t=1892',
                    'https://www.carrefour.fr/p/tomate-ronde-en-grappe-bio-carrefour-bio-3523680277724?t=1892',
                    'https://www.carrefour.fr/p/tomates-cerises-rondes-bio-3523680258358?t=1892',
                    'https://www.carrefour.fr/p/poireaux-bio-carrefour-bio-3276550020387?t=1892',
                    'https://www.carrefour.fr/p/carottes-bio-3523680271616?t=1892',
                    'https://www.carrefour.fr/p/salade-mache-bio-carrefour-bio-3523680425118?t=1892',
                    'https://www.carrefour.fr/p/pommes-de-terre-primeur-rikea-bio-3523680322042?t=1892',
                    'https://www.carrefour.fr/p/patate-douce-bio-3523680298378?t=1892',
                    'https://www.carrefour.fr/p/oignons-jaunes-bio-carrefour-bio-3276550103868?t=1892',
                    'https://www.carrefour.fr/p/potiron-bio-tranche-carrefour-bio-3276550320012?t=1892',
                    'https://www.carrefour.fr/p/gingembre-bio-3276559895733?t=1892',
                    'https://www.carrefour.fr/p/champignons-bruns-bio-carrefour-bio-3523680256637?t=1892',
                    'https://www.carrefour.fr/p/champignons-blancs-bio-carrefour-bio-3276550309857?t=1892',
                    'https://www.carrefour.fr/p/champignons-de-paris-blancs-carrefour-3276559134931?t=1892',
                    'https://www.carrefour.fr/p/salade-sucrine-3523680464926?t=1892',
                    'https://www.carrefour.fr/p/courgettes-3276550077565?t=1892',
                    'https://www.carrefour.fr/p/poivron-vert-3523680457256?t=1892',
                    'https://www.carrefour.fr/p/poivron-rouge-3523680457249?t=1892',
                    'https://www.carrefour.fr/p/salade-laitue-iceberg-3276559823125?t=1892',
                    'https://www.carrefour.fr/p/tomates-cerises-rouges-rondes-3276558396514?t=1892',
                    'https://www.carrefour.fr/p/chou-fleur-3000001038436?t=1892',
                    'https://www.carrefour.fr/p/pommes-de-terre-primeur-de-noirmoutier-igp-3276559251096?t=1892',
                    'https://www.carrefour.fr/p/pommes-de-terre-primeur-reflets-de-france-3523680298576?t=1892',
                    'https://www.carrefour.fr/p/pommes-de-terre-de-consommation-amandine-3523680431164?t=1892',
                    'https://www.carrefour.fr/p/pommes-de-terre-de-consommation-prunelle-filiere-qualite-carrefour-3276550480792?t=1892',
                    'https://www.carrefour.fr/p/asperges-pointes-vertes-3276559597507?t=1892',
                    'https://www.carrefour.fr/p/asperges-blanches-reflets-de-france-3276555494497?t=1892',
                    'https://www.carrefour.fr/p/asperges-vertes-3276555376397?t=1892',
                    'https://www.carrefour.fr/p/haricots-coco-plats-3276558134772?t=1892',
                    'https://www.carrefour.fr/p/haricots-verts-sans-fils-3523680340152?t=1892',
                    'https://www.carrefour.fr/p/brocoli-3276559825549?t=1892',
                    'https://www.carrefour.fr/p/epinards-jeunes-pousses-3523680444188?t=1892',
                    'https://www.carrefour.fr/p/oignons-jaunes-3276554574848?t=1892'
                     ]

    percent_carrefour = 0

    for url in url_legume_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[2]').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('legume')
            
            enseigne.append('carrefour')
            
            origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_legume_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les legumes de Carrefour :',percent_carrefour/len(url_legume_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="205"]/div[1]/section/article[2]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[3]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[4]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[5]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[15]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[26]/a/div[2]/h1',
        '//*[@id="205"]/div[1]/section/article[41]/a/div[2]/h1',
        
        '//*[@id="205"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="205"]/div[2]/section/article[2]/a/div[2]/h1',
        '//*[@id="205"]/div[2]/section/article[8]/a/div[2]/h1',
        '//*[@id="205"]/div[2]/section/article[10]/a/div[2]/h1',
        
        '//*[@id="205"]/div[3]/section/article[1]/a/div[2]/h1',
        '//*[@id="205"]/div[3]/section/article[2]/a/div[2]/h1',
        '//*[@id="205"]/div[3]/section/article[4]/a/div[2]/h1',
        
        '//*[@id="205"]/div[4]/section/article[1]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[2]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[7]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[12]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[21]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[23]/a/div[2]/h1',
        '//*[@id="205"]/div[4]/section/article[24]/a/div[2]/h1',
        
        '//*[@id="205"]/div[5]/section/article[9]/a/div[2]/h1',
        '//*[@id="205"]/div[5]/section/article[11]/a/div[2]/h1',
        '//*[@id="205"]/div[5]/section/article[22]/a/div[2]/h1',
        '//*[@id="205"]/div[5]/section/article[23]/a/div[2]/h1',
        '//*[@id="205"]/div[5]/section/article[30]/a/div[2]/h1',
        
        '//*[@id="205"]/div[7]/section/article[1]/a/div[2]/h1',
        '//*[@id="205"]/div[7]/section/article[4]/a/div[2]/h1',
        
        '//*[@id="205"]/div[9]/section/article[1]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[3]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[24]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[29]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[41]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[43]/a/div[2]/h1',
        '//*[@id="205"]/div[9]/section/article[44]/a/div[2]/h1',

        ]
    
    XPATH_prix = [
        '//*[@id="205"]/div[1]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[3]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[4]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[5]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[15]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[26]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[1]/section/article[41]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[2]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[2]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[2]/section/article[8]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[2]/section/article[10]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[3]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[3]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[3]/section/article[4]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[4]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[2]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[7]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[12]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[21]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[23]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[4]/section/article[24]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[5]/section/article[9]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[5]/section/article[11]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[5]/section/article[22]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[5]/section/article[23]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[5]/section/article[30]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[7]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[7]/section/article[4]/a/div[2]/p/span[2]',
        
        '//*[@id="205"]/div[9]/section/article[1]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[3]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[24]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[29]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[41]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[43]/a/div[2]/p/span[2]',
        '//*[@id="205"]/div[9]/section/article[44]/a/div[2]/p/span[2]',

        ]
    
    XPATH_quantite = [
        '//*[@id="205"]/div[1]/section/article[2]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[3]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[4]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[5]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[15]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[25]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[1]/section/article[41]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[2]/section/article[1]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[2]/section/article[2]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[2]/section/article[8]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[2]/section/article[10]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[3]/section/article[1]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[3]/section/article[2]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[3]/section/article[4]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[4]/section/article[1]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[2]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[7]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[12]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[21]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[23]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[4]/section/article[24]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[5]/section/article[9]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[5]/section/article[11]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[5]/section/article[22]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[5]/section/article[23]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[5]/section/article[30]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[7]/section/article[1]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[7]/section/article[4]/a/div[2]/p/span[1]',
        
        '//*[@id="205"]/div[9]/section/article[1]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[3]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[24]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[29]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[42]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[43]/a/div[2]/p/span[1]',
        '//*[@id="205"]/div[9]/section/article[44]/a/div[2]/p/span[1]',
        ]
    
    driver.get('https://www.labellevie.com/categorie/205/legumes')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append(clean_article(pays))
        
            categorie.append('legume')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,XPATH_quantite[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/205/legumes')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les legumes de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)




def extraction_pain():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_pain_carrefour = [
                    'https://www.carrefour.fr/p/baguette-carrefour-bio-3276559526392?t=1952',
                    'https://www.carrefour.fr/p/pain-boule-bio-carrefour-bio-2023040000050?t=1952',
                    'https://www.carrefour.fr/p/pain-complet-carrefour-bio-3523680347816?t=1952',
                    'https://www.carrefour.fr/p/baguette-bio-aux-graines-carrefour-bio-3523680353671?t=1952',
                    'https://www.carrefour.fr/p/pain-pave-carrefour-bio-3276556374927?t=1952',
                    'https://www.carrefour.fr/p/pain-campagnard-filiere-qualite-carrefour-3276559526507?t=1952'
                    ]

    percent_carrefour = 0

    for url in url_pain_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div[2]/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('pain')
            
            enseigne.append('carrefour')
            
            origine.append('france')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_pain_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour le pain de Carrefour :',percent_carrefour/len(url_pain_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="6419"]/div[1]/section/article[1]/a/div[2]/h1',
        '//*[@id="6419"]/div[1]/section/article[3]/a/div[2]/h1',
        '//*[@id="6419"]/div[1]/section/article[8]/a/div[2]/h1',
        '//*[@id="6419"]/div[1]/section/article[10]/a/div[2]/h1'
        

        ]
    
    XPATH_prix = [
        '//*[@id="6419"]/div[1]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6419"]/div[1]/section/article[3]/a/div[2]/p/span',
        '//*[@id="6419"]/div[1]/section/article[8]/a/div[2]/p/span',
        '//*[@id="6419"]/div[1]/section/article[10]/a/div[2]/p/span'
        ]
    
    
    driver.get('https://www.labellevie.com/categorie/6419/les-pains-de-boulanger')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            produit = driver.find_element(By.XPATH,XPATH_articles[i]).text
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('pain')
        
            enseigne.append('La belle vie')
            
            try:
            
                quantite.append(clean_quantite(produit))
                
            except:
                
                quantite.append('unité')
        
            lien.append('https://www.labellevie.com/categorie/6419/les-pains-de-boulanger')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour le pain de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)




def extraction_fromage():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_fromage_carrefour = [
                    'https://www.carrefour.fr/p/fromage-de-chevre-soignon-3523230028431?t=28129',
                    'https://www.carrefour.fr/p/fromage-coeur-complice-doux-et-cremeux-carrefour-3270190021278?t=28129',
                    'https://www.carrefour.fr/p/fromage-le-carre-cremeux-carrefour-classic-3560070789078?t=28129',
                    'https://www.carrefour.fr/p/comte-au-lait-cru-aop-carrefour-extra-3560070930128?t=28129',
                    'https://www.carrefour.fr/p/emmental-francais-carrefour-classic-3560071245962?t=28129',
                    'https://www.carrefour.fr/p/coulommiers-doux-et-cremeux-carrefour-3270190021148?t=28129',
                    'https://www.carrefour.fr/p/fromage-comte-bio-aop-juraflore-3542860082255?t=28129',
                    'https://www.carrefour.fr/p/fromage-emmental-bio-fremmental-om-bio-3227130705378?t=28129',
                    'https://www.carrefour.fr/p/fromage-cantal-bio-entre-deux-au-lait-cru-aop-3760051521028?t=28129',
                    'https://www.carrefour.fr/p/fromage-de-chevre-bio-3760014991905?t=28129',
                    'https://www.carrefour.fr/p/fromage-fourme-d-ambert-aop-bio-3277594787182?t=28129',
                    'https://www.carrefour.fr/p/mimolette-6-mois-d-affinage-bio-isigny-sainte-mere-3254550031909?t=28129',
                    'https://www.carrefour.fr/p/fromage-petit-camembert-bio-au-lait-cru-marie-harel-3267031601003?t=28129'
                     ]

    percent_carrefour = 0

    for url in url_fromage_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('fromage')
            
            enseigne.append('carrefour')
            
            origine.append('france')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_fromage_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les fromages de Carrefour :',percent_carrefour/len(url_fromage_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="6104"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="6104"]/div[2]/section/article[2]/a/div[2]/h1',
        '//*[@id="6104"]/div[2]/section/article[5]/a/div[2]/h1',
        '//*[@id="6104"]/div[2]/section/article[10]/a/div[2]/h1',
        '//*[@id="6104"]/div[2]/section/article[13]/a/div[2]/h1',
        
        '//*[@id="6104"]/div[3]/section/article[1]/a/div[2]/h1',
        '//*[@id="6104"]/div[3]/section/article[4]/a/div[2]/h1',
        '//*[@id="6104"]/div[3]/section/article[6]/a/div[2]/h1',
        
        '//*[@id="6104"]/div[4]/section/article[1]/a/div[2]/h1',
        '//*[@id="6104"]/div[4]/section/article[2]/a/div[2]/h1',
        '//*[@id="6104"]/div[4]/section/article[6]/a/div[2]/h1',
        
        ]
    
    XPATH_prix = [
        '//*[@id="6104"]/div[2]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6104"]/div[2]/section/article[2]/a/div[2]/p/span',
        '//*[@id="6104"]/div[2]/section/article[5]/a/div[2]/p/span',
        '//*[@id="6104"]/div[2]/section/article[10]/a/div[2]/p/span',
        '//*[@id="6104"]/div[2]/section/article[13]/a/div[2]/p/span',
        
        '//*[@id="6104"]/div[3]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6104"]/div[3]/section/article[4]/a/div[2]/p/span',
        '//*[@id="6104"]/div[3]/section/article[6]/a/div[2]/p/span',
        
        '//*[@id="6104"]/div[4]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6104"]/div[4]/section/article[2]/a/div[2]/p/span',
        '//*[@id="6104"]/div[4]/section/article[6]/a/div[2]/p/span',
        
        
        ]

    
    driver.get('https://www.labellevie.com/categorie/6104/les-fromages-de-grande-distribution')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('fromage')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6104/les-fromages-de-grande-distribution')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les fromages de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)





def extraction_cremerie():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_cremerie_carrefour = [
                    'https://www.carrefour.fr/p/oeufs-bio-de-plein-air-calibre-moyen-carrefour-bio-3270190021179?t=28128',
                    'https://www.carrefour.fr/p/creme-legere-semi-epaisse-18-mg-carrefour-classic-3245411851149?t=28128',
                    'https://www.carrefour.fr/p/oeufs-plein-air-carrefour-original-3270190205685?t=28128',
                    'https://www.carrefour.fr/p/margarine-tartine-et-cuisson-carrefour-3270190207573?t=28128',
                    'https://www.carrefour.fr/p/beurre-gastronomique-doux-carrefour-classic-3270190020288?t=28128',
                    'https://www.carrefour.fr/p/creme-fraiche-epaisse-entiere-carrefour-classic-3270190021001?t=28128',
                    'https://www.carrefour.fr/p/oeufs-frais-poules-plein-air-carrefour-original-3270190205678?t=28128',
                    'https://www.carrefour.fr/p/lait-demi-ecreme-de-nos-campagnes-classic-3560071080914?t=28128',
                    'https://www.carrefour.fr/p/lait-facile-a-digerer-carrefour-classic-3560070437405?t=28128',
                    'https://www.carrefour.fr/p/beurre-demi-sel-tendre-president-3155250366974?t=28128',
                    'https://www.carrefour.fr/p/creme-fouettee-legere-20-mat-gr-bridelice-3155250362655?t=28128',
                    'https://www.carrefour.fr/p/creme-fluide-bio-legere-15-mat-gr-bridelice-3155251208716?t=28128',
                    'https://www.carrefour.fr/p/creme-fouettee-ferme-et-onctueuse-president-3155250349793?t=28128',
                    'https://www.carrefour.fr/p/creme-fluide-legere-12-mat-gr-bridelice-3155250367858?t=28128'
                     ]

    percent_carrefour = 0

    for url in url_cremerie_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('cremerie')
            
            enseigne.append('carrefour')
            
            origine.append('france')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_cremerie_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les cremeries de Carrefour :',percent_carrefour/len(url_cremerie_carrefour)*100,'%')
    
    
    
    

    progression = 0
    
    
    
    
    
    
    XPATH_articles = [
        '//*[@id="6035"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="6035"]/div[2]/section/article[2]/a/div[2]/h1',
        '//*[@id="6035"]/div[2]/section/article[9]/a/div[2]/h1',
        '//*[@id="6035"]/div[2]/section/article[11]/a/div[2]/h1',
        
        '//*[@id="6035"]/div[4]/section/article[1]/a/div[2]/h1',
        '//*[@id="6035"]/div[4]/section/article[6]/a/div[2]/h1'
        ]
    
    XPATH_prix = [
        '//*[@id="6035"]/div[2]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6035"]/div[2]/section/article[2]/a/div[2]/p/span',
        '//*[@id="6035"]/div[2]/section/article[9]/a/div[2]/p/span',
        '//*[@id="6035"]/div[2]/section/article[11]/a/div[2]/p/span',
        
        '//*[@id="6035"]/div[4]/section/article[1]/a/div[2]/h1',
        '//*[@id="6035"]/div[4]/section/article[6]/a/div[2]/h1'
        ]

    
    driver.get('https://www.labellevie.com/categorie/6035/beurres-margarines')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('cremerie')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6035/beurres-margarines')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/','18')
        
        time.sleep(5)
        
        
        
        
        
        
        
    XPATH_articles = [
        '//*[@id="6036"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="6036"]/div[2]/section/article[4]/a/div[2]/h1',
        '//*[@id="6036"]/div[2]/section/article[7]/a/div[2]/h1',
        '//*[@id="6036"]/div[2]/section/article[11]/a/div[2]/h1',
        
        '//*[@id="6036"]/div[4]/section/article[1]/a/div[2]/h1',
        '//*[@id="6036"]/div[4]/section/article[2]/a/div[2]/h1'

        ]
    
    XPATH_prix = [
        '//*[@id="6036"]/div[2]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6036"]/div[2]/section/article[4]/a/div[2]/p/span',
        '//*[@id="6036"]/div[2]/section/article[7]/a/div[2]/p/span',
        '//*[@id="6036"]/div[2]/section/article[11]/a/div[2]/p/span',
        
        '//*[@id="6036"]/div[4]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6036"]/div[4]/section/article[2]/a/div[2]/p/span'
        ]

    
    driver.get('https://www.labellevie.com/categorie/6036/cremes-chantilly')
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('cremerie')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6036/cremes-chantilly')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/','18')
        
        time.sleep(5)
        
        
        
        
        
    XPATH_articles = [
        '//*[@id="6037"]/div[1]/section/article[1]/a/div[2]/h1',
        '//*[@id="6037"]/div[1]/section/article[2]/a/div[2]/h1'
        
        '//*[@id="6037"]/div[2]/section/article[2]/a/div[2]/h1',
        '//*[@id="6037"]/div[2]/section/article[10]/a/div[2]/h1'
        ]
    
    XPATH_prix = [
        '//*[@id="6037"]/div[1]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6037"]/div[1]/section/article[2]/a/div[2]/p/span',
        
        '//*[@id="6037"]/div[2]/section/article[2]/a/div[2]/p/span',
        '//*[@id="6037"]/div[2]/section/article[10]/a/div[2]/p/span'
        ]

    
    driver.get('https://www.labellevie.com/categorie/6037/laits-boissons-vegetales-et-lactees')
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('cremerie')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6037/laits-boissons-vegetales-et-lactees')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/','18')
        
        time.sleep(5)
        
    
    
    
    
    
    XPATH_articles = [
        '//*[@id="6038"]/div[1]/section/article[1]/a/div[2]/h1',
        '//*[@id="6038"]/div[1]/section/article[4]/a/div[2]/h1',
        
        '//*[@id="6038"]/div[2]/section/article[1]/a/div[2]/h1',
        '//*[@id="6038"]/div[2]/section/article[3]/a/div[2]/h1',
        
        '//*[@id="6038"]/div[3]/section/article[1]/a/div[2]/h1',
        '//*[@id="6038"]/div[3]/section/article[3]/a/div[2]/h1'
        ]
    
    XPATH_prix = [
        '//*[@id="6038"]/div[1]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6038"]/div[1]/section/article[4]/a/div[2]/p/span',
        
        '//*[@id="6038"]/div[2]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6038"]/div[2]/section/article[3]/a/div[2]/p/span',
        
        '//*[@id="6038"]/div[3]/section/article[1]/a/div[2]/p/span',
        '//*[@id="6038"]/div[3]/section/article[3]/a/div[2]/p/span'
        ]

    
    driver.get('https://www.labellevie.com/categorie/6038/oeufs')
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('france')
        
            categorie.append('cremerie')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6038/oeufs')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/','18')
        
        time.sleep(5)
        
        
        
        
    print('Pourcentage de réussite du scraper pour les fromages de La Belle Vie :',percent_lbv/18*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)





def extraction_viande():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_viande_carrefour = [
                    'https://www.carrefour.fr/p/viande-hachee-pur-boeuf-5-mg-carrefour-le-marche-3245415074230?t=1922',
                    'https://www.carrefour.fr/p/carpaccio-de-boeuf-basilic-charal-3181232180559?t=1922',
                    'https://www.carrefour.fr/p/chipolatas-longues-superieures-carrefour-3245415882897?t=1922',
                    'https://www.carrefour.fr/p/brochette-de-saucisses-mini-chipolatas-merguez-herbes-tendre-et-plus-3265980164372?t=1922',
                    'https://www.carrefour.fr/p/steak-hache-pur-boeuf-5-mg-carrefour-bio-3245415327282?t=1922',
                    'https://www.carrefour.fr/p/viande-hachee-bio-pur-boeuf-15-mg-carrefour-bio-3245415327404?t=1922',
                    'https://www.carrefour.fr/p/viande-bovine-entrecote-a-griller-carrefour-bio-3245415860628?t=1922',
                    'https://www.carrefour.fr/p/cotes-de-porc-bio-carrefour-bio-3270190215868?t=1922',
                    'https://www.carrefour.fr/p/viande-de-porc-filet-mignon-a-rotir-3276559976593?t=1922',
                    'https://www.carrefour.fr/p/viande-bovine-roti-a-griller-3276551122042?t=1922',
                    'https://www.carrefour.fr/p/saucisse-de-francfort-fumee-3523680266070?t=1922',
                    'https://www.carrefour.fr/p/viande-bovine-tartare-5-mg-et-sa-sauce-charal-3181232220279?t=1922',
                    'https://www.carrefour.fr/p/poitrine-de-porc-filiere-qualite-carrefour-3245415687157?t=1922',
                    'https://www.carrefour.fr/p/paupiettes-de-porc-carrefour-le-marche-3245415911689?t=1922',
                    'https://www.carrefour.fr/p/ribs-barbecue-original-madrange-3273625827100?t=1922',
                    'https://www.carrefour.fr/p/cuisses-manchons-de-canard-le-gaulois-3266980006433?t=1922',
                    'https://www.carrefour.fr/p/viande-bovine-steak-a-griller-3276551174805?t=1922',
                    'https://www.carrefour.fr/p/filets-de-poulet-5413458017578?t=1931',
                    'https://www.carrefour.fr/p/pilons-de-poulet-5413458017585?t=1931',
                    'https://www.carrefour.fr/p/filets-de-poulet-en-lanieres-5413458066880?t=1931',
                     ]

    percent_carrefour = 0

    for url in url_viande_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('viande')
            
            enseigne.append('carrefour')
            
            origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_viande_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour la viande de Carrefour :',percent_carrefour/len(url_viande_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="3869"]/div[5]/section/article[3]/a/div[2]/h1',
        '//*[@id="3869"]/div[5]/section/article[7]/a/div[2]/h1',
        '//*[@id="3869"]/div[5]/section/article[14]/a/div[2]/h1',
        '//*[@id="3869"]/div[5]/section/article[15]/a/div[2]/h1',
        '//*[@id="3869"]/div[5]/section/article[20]/a/div[2]/h1',
        '//*[@id="3869"]/div[5]/section/article[21]/a/div[2]/h1',
        
        
        
        '//*[@id="3869"]/div[10]/section/article[1]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[2]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[10]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[16]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[18]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[23]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[24]/a/div[2]/h1',
        '//*[@id="3869"]/div[10]/section/article[27]/a/div[2]/h1',
        
        ]
    
    XPATH_prix = [
        '//*[@id="3869"]/div[5]/section/article[3]/a/div[2]/p/span',
        '//*[@id="3869"]/div[5]/section/article[7]/a/div[2]/p/span',
        '//*[@id="3869"]/div[5]/section/article[14]/a/div[2]/p/span',
        '//*[@id="3869"]/div[5]/section/article[15]/a/div[2]/p/span',
        '//*[@id="3869"]/div[5]/section/article[20]/a/div[2]/p/span',
        '//*[@id="3869"]/div[5]/section/article[21]/a/div[2]/p/span',
        
        

        
        '//*[@id="3869"]/div[10]/section/article[31/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[2]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[10]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[16]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[18]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[23]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[24]/a/div[2]/p/span',
        '//*[@id="3869"]/div[10]/section/article[27]/a/div[2]/p/span',
        ]

    
    driver.get('https://www.labellevie.com/categorie/3869/boucherie')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append(None)
        
            categorie.append('viande')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/3869/boucherie')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les fromages de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)



def extraction_poisson():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_poisson_carrefour = [
                    'https://www.carrefour.fr/p/encornet-en-lamelles-3000000111314?t=1938',
                    'https://www.carrefour.fr/p/tranche-de-thon-albacore-decongelee-3276557312034?t=1938',
                    'https://www.carrefour.fr/p/filets-de-colin-d-alaska-facon-meuniere-carrefour-3523680434370?t=1938',
                    'https://www.carrefour.fr/p/paves-de-saumon-avec-peau-sans-aretes-filiere-qualite-carrefour-3523680308831?t=1938',
                    'https://www.carrefour.fr/p/crevettes-bio-entieres-cuites-carrefour-bio-3523680338296?t=1938',
                    'https://www.carrefour.fr/p/paves-de-saumon-carrefour-bio-3523680345249?t=1938',
                    'https://www.carrefour.fr/p/gambas-bio-decortiquees-cuites-carrefour-bio-3523680467316?t=1938',
                    'https://www.carrefour.fr/p/crevettes-decortiquees-delpierre-3336374402247?t=1938',
                    'https://www.carrefour.fr/p/filet-merlan-sans-aretes-carrefour-3523680296671?t=1938',
                    'https://www.carrefour.fr/p/crevettes-gambas-decortiquees-asc-delpierre-3336374401134?t=1938',
                    'https://www.carrefour.fr/p/moules-de-cordes-carrefour-bio-3523680429826?t=1938',
                    'https://www.carrefour.fr/p/dos-de-lieu-noir-msc-3276555177741?t=1938',
                    'https://www.carrefour.fr/p/pave-de-saumon-asc-filiere-qualite-carrefour-3276558790824?t=1938',
                    'https://www.carrefour.fr/p/huitres-marennes-oleron-igp-n04-filiere-qualite-carrefour-3523680421141?t=1938'
                     ]

    percent_carrefour = 0

    for url in url_poisson_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('poisson')
            
            enseigne.append('carrefour')
            
            origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_poisson_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour la viande de Carrefour :',percent_carrefour/len(url_poisson_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
       '//*[@id="6522"]/div[1]/section/article[1]/a/div[2]/h1'
        ]
    
    XPATH_prix = [
       '//*[@id="6522"]/div[1]/section/article[1]/a/div[2]/p/span'
        ]

    
    driver.get('https://www.labellevie.com/categorie/6522/poissons-fumes-caviar-et-oeufs-de-poissons')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('Norvege')
        
            categorie.append('poisson')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/6522/poissons-fumes-caviar-et-oeufs-de-poissons')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les fromages de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)
         


def extraction_feculent():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_feculent_carrefour = [
                    'https://www.carrefour.fr/p/riz-micro-ondes-basmati-1mn30-crf-3560070166046?t=2143',
                    'https://www.carrefour.fr/p/riz-basmati-carrefour-3560070837984?t=2143',
                    'https://www.carrefour.fr/p/pates-fusilli-carrefour-3560070329038?t=2143',
                    'https://www.carrefour.fr/p/riz-long-grain-10mn-carrefour-3560070822294?t=2143',
                    'https://www.carrefour.fr/p/ble-delicat-carrefour-3270190195474?t=2143',
                    'https://www.carrefour.fr/p/pates-spaghetti-carrefour-3560070328888?t=2143',
                    'https://www.carrefour.fr/p/pates-macaroni-carrefour-3560070329151?t=2143',
                    'https://www.carrefour.fr/p/polenta-grains-moyens-sans-gluten-alpina-savoie-3252971420319?t=2143',
                    'https://www.carrefour.fr/p/pates-al-bronzo-mezzi-rigatoni-barilla-8076809580861',
                    'https://www.carrefour.fr/p/pates-lasagne-geante-tezier-3259748000842?t=2143',
                    'https://www.carrefour.fr/p/pates-fusilli-al-bronzo-barilla-8076809581097',
                    'https://www.carrefour.fr/p/pates-fettuccine-panzani-3038359003301?t=2143',
                    'https://www.carrefour.fr/p/pates-tortiglioni-barilla-8076802085837?t=2143'
                     ]

    percent_carrefour = 0

    for url in url_feculent_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('feculent')
            
            enseigne.append('carrefour')
            
            origine.append('France')
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_feculent_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les feculents de Carrefour :',percent_carrefour/len(url_feculent_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="4590"]/div[2]/section/article[2]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[3]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[4]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[5]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[6]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[17]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[20]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[21]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[31]/a/div[2]/h1',
        '//*[@id="4590"]/div[2]/section/article[32]/a/div[2]/h1',
        ]
    
    XPATH_prix = [
        '//*[@id="4590"]/div[2]/section/article[2]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[3]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[4]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[5]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[6]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[17]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[20]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[21]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[31]/a/div[2]/p/span',
        '//*[@id="4590"]/div[2]/section/article[32]/a/div[2]/p/span',
        
        ]

    
    driver.get('https://www.labellevie.com/categorie/4590/pates-nouilles-riz')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append('France')
        
            categorie.append('feculent')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/4590/pates-nouilles-riz')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les feculents de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)
        



def extraction_huile():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_huile_carrefour = [
                    'https://www.carrefour.fr/p/huile-de-tournesol-livingwell-5430002928746?t=2157',
                    'https://www.carrefour.fr/p/vinaigre-de-vin-rouge-carrefour-classic-3270190006763?t=2157',
                    'https://www.carrefour.fr/p/huile-d-olive-vierge-extra-carrefour-extra-3560070854998?t=2157',
                    'https://www.carrefour.fr/p/vinaigre-de-cidre-carrefour-classic-3270190006794?t=2157',
                    'https://www.carrefour.fr/p/huile-d-olive-vierge-extra-carrefour-extra-3560071183684?t=2157',
                    'https://www.carrefour.fr/p/huile-vegetale-pepins-de-raisin-3155700000199?t=2157'
                     ]

    percent_carrefour = 0

    for url in url_huile_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('huile')
            
            enseigne.append('carrefour')
            
            try :
                
                origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            except:
                
                origine.append(None)
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_huile_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour l\'huile de Carrefour :',percent_carrefour/len(url_huile_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="4593"]/div[3]/section/article[1]/a/div[2]/h1',
        '//*[@id="4593"]/div[3]/section/article[8]/a/div[2]/h1',
        '//*[@id="4593"]/div[3]/section/article[12]/a/div[2]/h1',
        '//*[@id="4593"]/div[3]/section/article[19]/a/div[2]/h1'
        ]
    
    XPATH_prix = [
        '//*[@id="4593"]/div[3]/section/article[1]/a/div[2]/p/span',
        '//*[@id="4593"]/div[3]/section/article[8]/a/div[2]/p/span',
        '//*[@id="4593"]/div[3]/section/article[12]/a/div[2]/p/span',
        '//*[@id="4593"]/div[3]/section/article[19]/a/div[2]/p/span'
        ]

    
    driver.get('https://www.labellevie.com/categorie/4593/huiles-et-vinaigres')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
            
            texte = driver.find_element(By.XPATH,XPATH_articles[i]).text
            
            produit, pays = separateur(texte)
    
            articles.append(clean_article(produit))
            
            origine.append(None)
        
            categorie.append('huile')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/4593/huiles-et-vinaigres')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour l\'huile de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)



def extraction_boisson():


    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    prix, articles, quantite, categorie, enseigne, origine, lien, date = [], [], [], [], [], [], [], []
    
    progression = 0
    
    url_boisson_carrefour = [
            'https://www.carrefour.fr/p/eau-minerale-naturelle-hepar-7613035974692?t=27071',
            'https://www.carrefour.fr/p/eau-gazeuse-minerale-naturelle-salvetat-3068320123271?t=27071',
            'https://www.carrefour.fr/p/eau-de-source-carrefour-3270190114123?t=27071',
            'https://www.carrefour.fr/p/eau-naturelle-finement-petillante-carrefour-3560071189259?t=27071',
            'https://www.carrefour.fr/p/eau-aromatisee-citron-classic-carrefour-3245411377816?t=27071',
            'https://www.carrefour.fr/p/eau-minerale-naturelle-evian-3068320011707?t=27071',
            'https://www.carrefour.fr/p/eau-gazeuse-rouge-badoit-3068320110103?t=27071',
            'https://www.carrefour.fr/p/eau-de-source-cristaline-3254380003756?t=27071',
            'https://www.carrefour.fr/p/eau-minerale-naturelle-saint-amand-3162855999995?t=27071',
            'https://www.carrefour.fr/p/biere-aromatisee-tequila-desperados-3119780268405?t=27070',
            'https://www.carrefour.fr/p/sirop-fraise-teisseire-3092718618971',
            'https://www.carrefour.fr/p/boisson-the-peche-ice-tea-lipton-3502110009531?t=27073',
            'https://www.carrefour.fr/p/boisson-energisante-red-bull-9002490210779'
                    ]

    percent_carrefour = 0

    for url in url_boisson_carrefour:
        
        try:
        
            driver.get(url)
        
            prix.append(clean_price(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[2]/div/div/div/div[1]/div[1]/div/span').text))
        
            articles.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h1').text))
            
            categorie.append('boisson')
            
            enseigne.append('carrefour')
            
            try :
                
                origine.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/h2').text))
            
            except:
                
                origine.append(None)
            
            quantite.append(clean_article(driver.find_element(By.XPATH,'//*[@id="data-produit-card"]/div[1]/div[1]/span').text))
            
            lien.append(url)
            
            date.append(datetime.today().strftime('%Y-%m-%d'))
            
            percent_carrefour += 1
        
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(url_boisson_carrefour))
        
        time.sleep(3)
        
    print('Pourcentage de réussite du scraper pour les boissons de Carrefour :',percent_carrefour/len(url_boisson_carrefour)*100,'%')

    progression = 0
    
    XPATH_articles = [
        '//*[@id="5085"]/div[1]/section/article[1]/a/div[2]/h1',
        '//*[@id="5085"]/div[1]/section/article[2]/a/div[2]/h1',
        '//*[@id="5085"]/div[1]/section/article[4]/a/div[2]/h1',
        '//*[@id="5085"]/div[1]/section/article[5]/a/div[2]/h1',
        '//*[@id="5085"]/div[1]/section/article[7]/a/div[2]/h1',
        '//*[@id="5085"]/div[1]/section/article[8]/a/div[2]/h1',
        ]
    
    XPATH_prix = [
        '//*[@id="5085"]/div[1]/section/article[1]/a/div[2]/p/span',
        '//*[@id="5085"]/div[1]/section/article[2]/a/div[2]/p/span',
        '//*[@id="5085"]/div[1]/section/article[4]/a/div[2]/p/span',
        '//*[@id="5085"]/div[1]/section/article[5]/a/div[2]/p/span',
        '//*[@id="5085"]/div[1]/section/article[7]/a/div[2]/p/span',
        '//*[@id="5085"]/div[1]/section/article[8]/a/div[2]/p/span',
        ]

    
    driver.get('https://www.labellevie.com/categorie/5085/eaux')
    
    driver.find_element(By.XPATH, '//*[@id="confidentiality-refuse-all"]').click()
    
    percent_lbv = 0
    
   
    for i in range(len(XPATH_prix)):
        
        try:
        
            prix.append(clean_price(driver.find_element(By.XPATH,XPATH_prix[i]).text))
    
            articles.append(clean_article(driver.find_element(By.XPATH,XPATH_articles[i]).text))
            
            origine.append(None)
        
            categorie.append('boisson')
        
            enseigne.append('La belle vie')
            
            quantite.append(clean_quantite(driver.find_element(By.XPATH,XPATH_articles[i]).text))
        
            lien.append('https://www.labellevie.com/categorie/5085/eaux')
        
            date.append(datetime.today().strftime('%Y-%m-%d'))
        
            percent_lbv += 1
            
        except:
            
            pass
        
        progression += 1
        
        print('Chargement :',progression,'/',len(XPATH_articles))
        
        time.sleep(5)
        
    print('Pourcentage de réussite du scraper pour les boissons de La Belle Vie :',percent_lbv/len(XPATH_articles)*100,'%')

    df = pd.DataFrame(list(zip(articles, categorie, enseigne, prix, quantite, origine, lien, date)), columns = ['Article', 'Type', 'Enseigne', 'Prix', 'Quantité', 'Origine', 'URL', 'Date'])
         
    return(df)


def final():
    
    df = (pd.concat([extraction_fruit(), extraction_legume(), extraction_boisson(), extraction_cremerie(), extraction_feculent(), extraction_fromage(), extraction_huile(), extraction_pain(), extraction_poisson(), extraction_viande()]))
    
    return(df)
         

        
        



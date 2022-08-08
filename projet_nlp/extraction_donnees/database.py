# Importation des librairies
from bs4 import BeautifulSoup
import requests
import pandas as pd

def clean_sentiment(str) :
    '''Permet de nettoyer le string'''
    str = str.replace(' ','')
    str = str.replace('\n','')
    return str

def scraping_avis() :
    '''Fonction à appeler pour générer la base de données'''
    
    ## Initialisation
    df = pd.DataFrame(columns=["Avis","Sentiment"])
    base = 'https://www.plus.transformation.gouv.fr'
    
    experiences = [] # contiendra la liste des URL de tous les avis
    service = [] # contiendra le nom du (ou des) service(s) associé(s) à l'avis
    avis = [] # contiendra l'avis (texte)
    sentiment = [] # contiendra le sentiment associéà l'avis (Positif, Négatif, Neutre)

    # Recherche de toutes les URL des avis utilisateurs
    for num_page in range(1,869) :
        url ='https://www.plus.transformation.gouv.fr/experiences?combine=&reponse=All&organisme=&page='
        req = requests.get(url+str(num_page), headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}).text
        soup = BeautifulSoup(req, "html.parser")
        card_link = soup.findAll(class_='fr-card__link',href=True)

        # Fins d'URL des expériences utilisateurs dans une liste
        for link in card_link :
            experiences.append(link['href'])

    progression = 0
    for exp in experiences :
        nb_avis = len(experiences)
        
        # On associe la base d'URL avec la fin d'URL associée à un avis utilisateur
        url = base+exp
        req = requests.get(url , headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}).text
        soup = BeautifulSoup(req, "html.parser")
        
        # Services ministériel associé à l'avis
        for serv in soup.findAll("span",{'class' : "experience-organization fr-mb-0 fr-text--lg fr-text--bold fr-text--uppercase"}) :
            service.append(serv.text)

        # Avis texte de l'utilisateur
        avis.append(soup.find("article").find("div").text)

        # Sentiment attribué (Positif, Négatif ou Neutre)
        sentiment.append(clean_sentiment(soup.find("div",{'class' : "experience-feeling-status fr-text--lg fr-text--bold fr-mb-4w"}).text))
            
        print("Progression : "+str(progression)+"/"+str(nb_avis))
    
    # Sauvegarde dans un DataFrame
    df["Service"] = service
    df["Avis"] = avis
    df["Sentiment"] = sentiment
    
    # Sauvegarde dans un fichier CSV
    df.to_csv('database.csv')   

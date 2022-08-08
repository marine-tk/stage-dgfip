## Importation des librairies

import tweepy

import pandas as pd

import re

import spacy

from spacy.tokens import Token

from unidecode import unidecode



## Tokenisation des tweets

def clear_tweet(tweet):
    
    nlp = spacy.load("fr_core_news_lg")
    
    tweet = nlp(tweet)
    
    handle_regex = r"@[\w\d_]+"
    
    like_handle = lambda token: re.fullmatch(handle_regex, token.text)
    
    Token.set_extension("like_handle", getter=like_handle, force=True)
    
    return [ unidecode(token.lemma_.lower()) for token in tweet 
        
                if (not token.is_punct) 
        
                and (not token.is_space) 
        
                and (not token.like_url) 
        
                and (not token.is_stop) 
        
                and len(token) > 1 
        
                and (not token.ent_type_ == "PER") 
        
                and (not token._.like_handle) ]
 
 
 
## Extraction des données 

def scrape(mot_clef, date, nb_tweet):
 
        ## Création d'un DataFrame
        df = pd.DataFrame(columns=['Nom d\'utilisateur',
                                   
                                   #'Geolocalisation',
                                   
                                   'Following',
                                   
                                   'Followers',
                                   
                                   'Nombre total de tweet',
                                   
                                   'Nombre de retweet',
                                   
                                   'Contenu brut',
                                   
                                   'Contenu tokenisé',
                                   
                                   'Hashtags',
                                   
                                   'Date'])
 
        ## Extraction des tweets
        tweets = tweepy.Cursor(identification().search_tweets,
                               
                               mot_clef, lang="fr",
                               
                               since_id=date,
                               
                               tweet_mode='extended').items(nb_tweet)
 
 
        ## Création d'une liste de tweet
        list_tweets = [tweet for tweet in tweets]
 
        ## Initialisation de compteur
        progression = 1
 
        ## Extraction de chaque donnée du tweet
        for tweet in list_tweets:
            
                username = tweet.user.screen_name
                
                #geo = tweet.coordinates
                
                following = tweet.user.friends_count
                
                followers = tweet.user.followers_count
                
                totaltweets = tweet.user.statuses_count
                
                retweetcount = tweet.retweet_count
                
                date = str(tweet.created_at)[0:10]
                
                hashtags = tweet.entities['hashtags']
 
                ## Distinction tweet/retweet et récupération de l'intégralité du texte
                try:
                    
                        text = tweet.retweeted_status.full_text
                        
                except AttributeError:
                    
                        text = tweet.full_text
                        
                hashtext = list()
                
                ## Tokenisation du texte
                text_tok = clear_tweet(text)
                
                ## Extraction des hastags
                for j in range(0, len(hashtags)):
                    
                        hashtext.append(hashtags[j]['text'])
 
                ith_tweet = [username, #geo,
                             
                             following,
                             
                             followers, totaltweets,
                             
                             retweetcount, text, text_tok, 
                             
                             hashtext, date]
                
                df.loc[len(df)] = ith_tweet
                
                print('Chargement :',progression,'/',nb_tweet)
                
                progression += 1
 
        return(df)
    
 
    
def identification():

    ## Cette fontion nous permet d'intéragir avec l'API Tweepy
 

        consumer_key = "EGj1VvBZp7P1TdxOKfr2VMdFN"
        
        consumer_secret = "m9rSsqQpeKjRpNuhFLAGcoq24nxCavZ2O0q6rGyyRA4CCOViBK"
        
        access_key = "1393204806370709506-Aw8ke3Ba919iXZavmt2EyFUQYK5QqN"
        
        access_secret = "NYouUSZJ5iMGVSWvh9Y06PyD3i8TFvTucIPBoV6ETI0AH"
 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        
        auth.set_access_token(access_key, access_secret)
        
        api = tweepy.API(auth)
 
 
        return(api)


def factorisation(df):

    ## Cette fonction nous permet de supprimer les doublons 
    
    new_df = df.copy()
    
    index_sup = []
    
    for i in range(len(df)):
        
        if i not in index_sup:
        
            liste_index = df[df["Contenu brut"] == df['Contenu brut'][i]].index.tolist()

            del liste_index[0]
        
            if len(liste_index) > 0:
        
                for i in range(len(liste_index)):
        
                    new_df = new_df.drop(liste_index[i])
                
                    index_sup.append(liste_index[i])
        
    return(new_df)
    
    
    
def enregistrement():
    
        
        print("Entrer le mot clef")
        
        mot_clef = input()
        
        print('\n')
        
        print("Entrer la date à partir de laquelle commencera l'extraction de tweets (aaaa-mm-jj)")
        
        date = input()
        
        print('\n')
        
        print("Entrer le nombre de tweet souhaités")
        
        nb_tweet = int(input())
    
        df = scrape(mot_clef, date, nb_tweet)
        
        df = factorisation(df)
        
        print('\n')
        
        print('Extraction des tweets terminée !')
        
        df.to_excel('extraction_tweet.xlsx')
        
        df.to_csv('extraction_tweet.csv')
        
        return(df)
        
        
        
        
        
        
        
        
        
        
        
        

# Importation des librairies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from google.cloud import storage

######################### Définition des chemins #########################
# Chemin où le script, key_file.json et le fichier CSV initial se trouvent
path = "/home/marinetk/scripts/"

# Chemin où sont enregistrés les fichiers CSV
path_prix = "/home/marinetk/prix_essence/"
path_valeur100 = "/home/marinetk/valeur_100_essence/"

# Dossier contenant les fichiers temporaires
path_tmp = "/home/marinetk/scripts/tmp/"
#########################################################################

def departement_price(text) :
    '''
    Fonction séparant dans une liste les prix de l'essence et le nom du département associé
    Par exemple text = "Ain (01)2,063€2,104€2,061€1,990€0,873€0,912€"
    Retour de la fonction  = ['Ain_01', [2.063, 2.104, 2.061, 1.99, 0.873]]
    '''
   
    list_price = []
    list_text = text.split('€')
    
    for text in list_text :
        if ')' in text :
            departement = text.split(')')[0]
            departement = departement.replace('(','_')
            departement = departement.replace(' ','')
            text = text.split(')')[1]
            
        text = text.replace(',','.')   
        if text != '' :
            list_price.append(float(text))
            
        list_price_sans_GPL = list_price[0:5]
        
    return [departement,list_price_sans_GPL]

def create_dataframe() :
    ''' Fonction permettant la création du DataFrame contenant les prix scrapés et le scraping '''
    
    # Scraping
    url = 'https://www.carburants.org/prix-carburants/'
    req = requests.get(url , headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}).text
    soup = BeautifulSoup(req, 'html.parser')
    all_tr = soup.findAll('tr')
    
    dict_departement = {}
    
    # 'tr' permet de trouver tous le contenu du tableau des prix
    all_tr = soup.findAll('tr')

    # Chaque elem (type : string) correspond à un département
    for elem in all_tr[1:len(all_tr)] : # (pour ne pas considérer la première ligne qui donne le nom des colonnes)
        if 'Corse' not in elem.text : # on ne considère pas la Corse
            
            nom_departement =  departement_price(elem.text)[0]
            prix =  departement_price(elem.text)[1]
            
            dict_departement[nom_departement] = prix
            
    df_essence = pd.DataFrame(dict_departement,index=['Gasoil','SP98','SP95','E10','E85'])
    
    return df_essence.T

def decomposition_prix_valeur():
    ''' Conversion en base 100 et création des fichiers CSV '''
    
    df_init = pd.read_csv(path+"essence_init_bis_05-07-2022.csv")
    df = create_dataframe()
    
    df.to_csv(path_tmp+"temporary_to_delete.csv")
    df = pd.read_csv(path_tmp+"temporary_to_delete.csv")
   
    new_df = df.copy()
    
    ### Calcul en base 100 dans new_df
   
    for i in range(1, df_init.shape[0]) : # on ne parcourt pas la ligne des dates
        for j in range(1,df_init.shape[1]) : # on ne parcourt pas le nom des départements
            #print(df_init.iloc[i,j])
            new_df.iloc[i,j] = round((float(df.iloc[i,j])/float(df_init.iloc[i,j]))*100,3)
            
    ### Enregistrement des fichiers CSV + ajout de la date
    
    df["Date"] = [datetime.today().strftime('%Y-%m-%d') for k in range(len(df))]
    new_df["Date"] = [datetime.today().strftime('%Y-%m-%d') for k in range(len(new_df))]
    
    df = df.rename(columns= {'Unnamed: 0' : 'Département'})
    new_df = new_df.rename(columns= {'Unnamed: 0' : 'Département'})
    
    df.to_csv(path_prix+'prix_essence' + datetime.today().strftime('%Y-%m-%d') + '.csv')
    print('Fichier des prix CSV enregistré')
   
    new_df.to_csv(path_valeur100+'valeur_100_essence' + datetime.today().strftime('%Y-%m-%d') + '.csv')
    print('Fichier valeur_100 CSV enregistré')

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Transfert du fichier blob_name, issu du répertoire path_to_file dans le bucket bucket_name """
     
    # Clé JSON générée sur GCP dans la rubrique IAM et admin
    storage_client = storage.Client.from_service_account_json(path+'key_file.json')

    
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    print("Le fichier a bien été enregistré dans le bucket ",bucket_name)
    
    return blob.public_url
 
def execute_all() :
  ''' Fonction finale qui fait appel à toutes les autres fonctions '''
  
  # Nom des fichiers le jour de son exécution
  prix_du_jour = 'prix_essence' + datetime.today().strftime('%Y-%m-%d') + '.csv'
  valeur100_du_jour = 'valeur_100_essence' + datetime.today().strftime('%Y-%m-%d') + '.csv'

  # Création des fichiers CSV
  decomposition_prix_valeur()

  # Transfert vers des buckets de Google Cloud Storage
  upload_to_bucket(prix_du_jour,path_prix+prix_du_jour,'prix-essence-csv')
  upload_to_bucket(valeur100_du_jour,path_valeur100+valeur100_du_jour,'valeur100-essence-csv')
    
#########################################################################

execute_all()

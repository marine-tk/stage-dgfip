# Importation des librairies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from google.cloud import storage

# Chemin où le script, key_file.json et le fichier CSV initial se trouvent
path = "/home/marinetk/scripts/"

# Chemin où sont enregistrés les fichiers CSV
path_prix = "/home/marinetk/prix_logement/"
path_valeur100 = "/home/marinetk/valeur_100_logement/"

# Dossier contenant les fichiers temporaires
path_tmp = "/home/marinetk/scripts/tmp/"

def clean(str) :
  '''Pour nettoyer le string et le convertir en flottant'''
  str = str.replace(' ','')
  str = str.replace('\n','')
  str = str.replace('€/L','')
  str = str.replace('€/U','')
  str = str.replace(',','.')
  str = str.replace('€/KG','')
  str = str.replace('€','')
  return float(str)

def extract_logement():
  sites =["https://www.drimki.fr/prix-immobilier/paris-75000",
               "https://www.drimki.fr/prix-immobilier/noisy-le-grand-93160",
               "https://www.drimki.fr/prix-immobilier/clermont-ferrand-63000",
               "https://www.drimki.fr/prix-immobilier/saint-denis-93200",
               "https://www.drimki.fr/prix-immobilier/bordeaux-33000",
               "https://www.drimki.fr/prix-immobilier/lille-59000",
               "https://www.drimki.fr/prix-immobilier/nice-06000",
               "https://www.drimki.fr/prix-immobilier/ussel-19200",
               "https://www.drimki.fr/prix-immobilier/epinal-88000",
               "https://www.drimki.fr/prix-immobilier/montech-82700",
               "https://www.drimki.fr/prix-immobilier/peronne-80200",
               "https://www.drimki.fr/prix-immobilier/limoges-87000",
               "https://www.drimki.fr/prix-immobilier/vichy-03200",
               "https://www.drimki.fr/prix-immobilier/digne-les-bains-04000",
               "https://www.drimki.fr/prix-immobilier/briancon-05100",
               "https://www.drimki.fr/prix-immobilier/cannes-06400",
               "https://www.drimki.fr/prix-immobilier/troyes-10000",
               "https://www.drimki.fr/prix-immobilier/carcassonne-11000",
               "https://www.drimki.fr/prix-immobilier/marseille-13000",
               "https://www.drimki.fr/prix-immobilier/caen-14000",
               "https://www.drimki.fr/prix-immobilier/la-rochelle-17000",
               "https://www.drimki.fr/prix-immobilier/dijon-21000",
               "https://www.drimki.fr/prix-immobilier/bourganeuf-23400",
               "https://www.drimki.fr/prix-immobilier/besancon-25000",
               "https://www.drimki.fr/prix-immobilier/montelimar-26200",
               "https://www.drimki.fr/prix-immobilier/brest-29200",
               "https://www.drimki.fr/prix-immobilier/nimes-30000",
               "https://www.drimki.fr/prix-immobilier/toulouse-31000",
               "https://www.drimki.fr/prix-immobilier/montpellier-34000",
               "https://www.drimki.fr/prix-immobilier/rennes-35200",
               "https://www.drimki.fr/prix-immobilier/chateauroux-36000",
               "https://www.drimki.fr/prix-immobilier/tours-37000",
               "https://www.drimki.fr/prix-immobilier/grenoble-38100",
               "https://www.drimki.fr/prix-immobilier/saint-etienne-42000",
               "https://www.drimki.fr/prix-immobilier/nantes-44000",
               "https://www.drimki.fr/prix-immobilier/reims-51100",
               "https://www.drimki.fr/prix-immobilier/nancy-54000",
               "https://www.drimki.fr/prix-immobilier/metz-57000",
               "https://www.drimki.fr/prix-immobilier/calais-62100",
               "https://www.drimki.fr/prix-immobilier/pau-64000",
               "https://www.drimki.fr/prix-immobilier/biarritz-64200",
               "https://www.drimki.fr/prix-immobilier/perpignan-66000",
               "https://www.drimki.fr/prix-immobilier/strasbourg-67200",
               "https://www.drimki.fr/prix-immobilier/mulhouse-68200",
               "https://www.drimki.fr/prix-immobilier/lyon-69000",
               "https://www.drimki.fr/prix-immobilier/annecy-74000",
               "https://www.drimki.fr/prix-immobilier/rouen-76000",
               "https://www.drimki.fr/prix-immobilier/versailles-78000",
               "https://www.drimki.fr/prix-immobilier/albi-81000",
               "https://www.drimki.fr/prix-immobilier/avignon-84000"]

  df_logement = pd.DataFrame(index=["Paris", "Noisy-le-Grand",
                                  "Clermont-Ferrand","Saint-Denis",
                                  "Bordeaux","Lille",
                                  "Nice","Ussel",
                                  "Epinal","Montech",
                                  "Peronne","Limoges",
                                  "Vichy","Digne-les-Bains",
                                  "Briancon","Cannes",
                                  "Troyes","Carcassonne",
                                  "Marseille","Caen",
                                  "La Rochelle","Dijon",
                                  "Bourganeuf","Besancon",
                                  "Montelimar","Brest",
                                  "Nîmes","Toulouse",
                                  "Montpellier","Rennes",
                                  "Châteauroux","Tours",
                                  "Grenoble","Saint-Etienne",
                                  "Nantes","Reims",
                                  "Nancy", "Metz",
                                  "Calais",
                                  "Pau","Biarritz",
                                  "Perpignan","Strasbourg",
                                  "Mulhouse","Lyon",
                                  "Annecy","Rouen",
                                  "Versailles","Albi",
                                  "Avignon"],
                           columns=['Prix au m²'])

  liste_prix = []
  chargement = 0

  for url in sites :
    req = requests.get(url , headers={'User-Agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(req, "html.parser")
    try :
        prix = soup.find('span', {'class' : "c_green d-block number font-weight-light"})
        liste_prix.append(clean(prix.text))
        chargement += 1
        print('Chargement :', 2*chargement , '/100')
    except :
        pass

  df_logement["Prix au m²"] = liste_prix
  df_logement = df_logement.sort_index().T
  df_logement["Date"] = [datetime.today().strftime('%Y-%m-%d')]

  return(df_logement)


## Création d'un DataFrame initial

def init_df():  
    df_init = pd.DataFrame(np.array([[1754,3943,2039,1751,5277,4252,290,
                                      1401,2051,2256,1398,4546,1024,887,
                                      1768,1360,2019,998,2284,3734,3120,
                                      1300,4234,2565,2452,1263,2823,1405,
                                      2403,1891,3176,3585,3631,1728,10008,
                                      1593,1086,1263,2120,2880,2295,3653,983,
                                      3314,2885,2233,1296,725,6117,1195]]),
                   
                           columns = ["Paris", "Noisy-le-Grand","Clermont-Ferrand",
                                      "Saint-Denis","Bordeaux","Lille","Nice","Ussel",
                                      "Epinal","Montech","Peronne","Limoges", "Vichy",
                                      "Digne-les-Bains","Briancon","Cannes","Troyes",
                                      "Carcassonne","Marseille","Caen","La Rochelle",
                                      "Dijon","Bourganeuf","Besancon","Montelimar","Brest",
                                      "Nîmes","Toulouse","Montpellier","Rennes","Châteauroux",
                                      "Tours","Grenoble","Saint-Etienne","Nantes","Reims","Nancy",
                                      "Metz","Calais","Pau","Biarritz","Perpignan","Strasbourg",
                                      "Mulhouse","Lyon","Annecy","Rouen","Versailles","Albi","Avignon"])
   
    return(df_init)


## Transformation en base 100

def decomposition_prix_valeur(df_init , df):
   
    new_df = df.copy()
   
    for i in range(len(df_init.T)):
        new_df.iloc[0,i] = round((df.iloc[0,i]/df_init.iloc[0,i])*100,3)

    df.to_csv(path_prix+'prix_logement' + datetime.today().strftime('%Y-%m-%d') + '.csv')
    print('CSV des prix des logements enregistré')

    new_df.to_csv(path_valeur100+'valeur_100_logement' + datetime.today().strftime('%Y-%m-%d') + '.csv')
    print('CSV des valeurs 100 des logements enregistré')


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
  prix_du_jour = 'prix_logement' + datetime.today().strftime('%Y-%m-%d') + '.csv'
  valeur100_du_jour = 'valeur_100_logement' + datetime.today().strftime('%Y-%m-%d') + '.csv'

  # Création des fichiers CSV
  decomposition_prix_valeur(init_df() , extract_logement())

  # Transfert vers des buckets de Google Cloud Storage
  upload_to_bucket(prix_du_jour,path_prix+prix_du_jour,'prix-logement-csv')
  upload_to_bucket(valeur100_du_jour,path_valeur100+valeur100_du_jour,'valeur100-logement-csv')
  

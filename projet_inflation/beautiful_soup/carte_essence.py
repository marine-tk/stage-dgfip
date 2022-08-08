### Importation des librairies
import geopandas
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable

####### À changer selon les besoins #######
date = '2022-08-05'      
carburant = 'E85'    
###########################################

### Importation des données du carburant

def importation():
    df = pd.read_csv('prix_essence' + date + '.csv') # choix du csv à une date donnée
    
    # On met tous les prix en flottant (qui étaient des string)
    df['Gasoil'] = df['Gasoil'].apply(float)
    df['SP98'] = df['SP98'].apply(float)  
    df['SP95'] = df['SP95'].apply(float)  
    df['E10'] = df['E10'].apply(float) 
    df['E85'] = df['E85'].apply(float)  

    # Par exemple, Val-d'Oise_95 devient Val-d'Oise
    df['nom'] = df['Département'].apply(lambda x: x[:len(x)-3])

    # On supprime les colonnes inutiles
    del df['Unnamed: 0']
    del df['Département']
    del df['Date']
    
    # Il manquait les espaces dans ce nom de département
    df.iloc[88,5] = 'Territoire de Belfort'
    return(df)

### Importation du fond de carte
def coordonees_departements():
    # Permet d'avoir la carte des départements
    url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"   
    geo = geopandas.read_file(url)  
    geo = geo.drop(48)   
    geo = geo.drop(73)   
    return(geo)

### Visualisation de la carte
def carte_brute():
    geo = coordonees_departements()   
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    geo.plot(ax=ax, color='white', edgecolor='black')   
    
def merge():   
    df = importation()   
    geo = coordonees_departements()  
    fusion = pd.merge(df, geo, how="right", left_on="nom", right_on="nom")  
    return(fusion, df, geo)

def carte_metropole(carburant):  
    '''
    Entrée : carburant est un string à choisir parmi :
    'Gasoil', 'SP98', 'SP95', 'E10', 'E85'
    ''' 
    fusion, df, geo = merge()   
    geomerged = geopandas.GeoDataFrame(fusion)   
    fig, ax = plt.subplots(figsize=(16,10))

    # ligne à ajouter pour avoir une légende ajustée à la taille du graphe
    cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.00001)

    geomerged.plot(column=carburant, ax=ax, edgecolor='black', legend=True, cmap ="BuPu", cax=cax)   
    plt.savefig('carte_metropole_'+carburant, dpi = 400)   
   
def carte_idf(carburant): 
    fusion, df, geo = merge()   
    fusion_idf = pd.DataFrame(columns = ['nom', carburant, 'geometry'])  
    
    idf = ['Paris',
           'Seine-et-Marne',
           'Yvelines',
           'Essonne',
           'Hauts-de-Seine',
           'Seine-Saint-Denis',
           'Val-de-Marne',
           "Val-d'Oise"]
    
    for i in fusion.index :  
        if fusion.iloc[i][5] in idf :
            fusion_idf = fusion_idf.append(fusion.loc[i])   

    geomerged = geopandas.GeoDataFrame(fusion_idf)
    
    fig, ax = plt.subplots(figsize=(16,16))

    geomerged.plot(column=carburant, ax=ax, edgecolor='black',
        legend=True, cmap="BuPu") #, cax=cax
    
    plt.savefig('carte_idf_'+carburant, dpi = 400)

carte_metropole(carburant)
carte_idf(carburant)

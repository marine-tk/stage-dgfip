#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:31:39 2022

@author: geoffroyperonne
"""

## Importation des librairies

import geopandas

import matplotlib.pyplot as plt

import pandas as pd

from mpl_toolkits.axes_grid1 import make_axes_locatable

import folium


## Importation des données du carburant

def importation():

    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet inflation/Table_jour/essence/prix_essence2022-07-05.csv')
    
    df = df.drop(0)
    
    df['Gasoil'] = df['Gasoil'].apply(float)
    
    df['SP98'] = df['SP98'].apply(float)
    
    df['SP95'] = df['SP95'].apply(float)
    
    df['E10'] = df['E10'].apply(float)
    
    df['E85'] = df['E85'].apply(float)
    
    del df['Unnamed: 0.1']
    
    df['nom'] = df['Unnamed: 0'].apply(lambda x: x[:len(x)-3])
    
    del df['Unnamed: 0']
    
    df.iloc[88,5] = 'Territoire de Belfort'
    
    return(df)


## Importation du fond de carte

def coordonees_departements():
    
    url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    
    geo = geopandas.read_file(url)
    
    geo = geo.drop(48) 
    
    geo = geo.drop(73) 
    
    return(geo)

## Visualisation de la carte

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
    
    fusion, df, geo = merge()
    
    geomerged = geopandas.GeoDataFrame(fusion)
    
    fig, ax = plt.subplots(figsize=(16,10))

    # ligne à ajouter pour avoir une légende ajustée à la taille du graphe

    cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.00001)

    geomerged.plot(column=carburant, ax=ax, edgecolor='black', legend=True, cmap ="BuPu", cax=cax)
    
    plt.savefig('carte_metropole_'+carburant, dpi = 400)
    
    
    
    
    
def carte_paris(carburant):
    
    fusion, df, geo = merge()
    
    fusion_paris = pd.DataFrame(columns = ['nom', carburant, 'geometry']) 
    
    for i in [36, 63, 37, 87, 44, 19, 66, 88]:
    
        fusion_paris = fusion_paris.append(fusion.loc[i])
    
    geomerged = geopandas.GeoDataFrame(fusion_paris)
    
    fig, ax = plt.subplots(figsize=(16,16))

    # ligne à ajouter pour avoir une légende ajustée à la taille du graphe

    #cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.1)

    geomerged.plot(column=carburant, ax=ax, edgecolor='black',
        legend=True, cmap="BuPu") #, cax=cax
    
    plt.savefig('carte_paris_'+carburant, dpi = 400)

    
    
    
    
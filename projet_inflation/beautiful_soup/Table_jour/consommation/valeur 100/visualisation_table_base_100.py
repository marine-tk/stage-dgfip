#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 13:56:36 2022

@author: geoffroyperonne
"""

## Importation des librairies

import pandas as pd


## On importe la base de données des bases 100

def importation():

    df = pd.read_csv('/Users/geoffroyperonne/Desktop/DGFiP/Projet inflation/Table:jour/consommation/valeur 100/valeur_base_100_total.csv')
    
    ## A changer en fonction des colonnes qu'on veut supprimer
    
    del df['string_field_0']
    del df['Cartouche_20_paquets']
    del df['Tabac_a_rouler_500g']
    del df['Nettoyant_vitre______L_']
    
    del df['Eponge______U_']
    del df['Dentifrice______L_']
    del df['Protection_hygi__nique______U_']
    del df['Pr__servatifs______U_']
    
    del df['Pates______kg_']
    del df['Eau______kg_']
    del df['Oeufs______kg_']
    del df['Paracetamol__bo__te_de_8_comprim__s_de_1000mg_']
    
    del df['Ibuprof__ne__bo__te_de_12_comprim__s_de_400mg_']
    del df['D__sinfectants__125mL_']
    
    return(df)




def classement_variance():
    
    df = importation()
    
    return(df.var())




def description():
    
    df = importation()
    
    return(df.describe().T)

    
    
    
    
    
    
    
    
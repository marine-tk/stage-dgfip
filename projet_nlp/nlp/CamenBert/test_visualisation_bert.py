#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 18:17:53 2022

@author: geoffroyperonne
"""

#%%

import numpy as np

import pandas as pd

from joblib import load

from sklearn.metrics import confusion_matrix

from keras.preprocessing.sequence import pad_sequences

from transformers import CamembertTokenizer

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import seaborn as sn

import matplotlib.pyplot as plt

import torch

#%%

def test(sentences):
    
    model = load('/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Bert/monpremiermodele.modele')
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Encode the comments
    tokenizer = CamembertTokenizer.from_pretrained('camembert-base',do_lower_case=True)
    
    tokenized_comments_ids = [tokenizer.encode(sentence,add_special_tokens=True,max_length=128) for sentence in sentences]
    
    # Pad the resulted encoded comments
    tokenized_comments_ids = pad_sequences(tokenized_comments_ids, maxlen=128, dtype="long", truncating="post", padding="post")

    # Create attention masks 
    attention_masks = []
    
    for seq in tokenized_comments_ids:
        
        seq_mask = [float(i>0) for i in seq]
        
        attention_masks.append(seq_mask)

    prediction_inputs = torch.tensor(tokenized_comments_ids)
    
    prediction_masks = torch.tensor(attention_masks)
    
    # Apply the finetuned model (Camembert)
    flat_pred = []
    
    with torch.no_grad():
        # Forward pass, calculate logit predictions
        outputs =  model(prediction_inputs.to(device),token_type_ids=None, attention_mask=prediction_masks.to(device))
        
        logits = outputs[0]
        
        logits = logits.detach().cpu().numpy() 
        
        flat_pred.extend(np.argmax(logits, axis=1).flatten())
        
    for i in range(len(flat_pred)):
        
        print('Comment: ', sentences[i])
        
        print('Label', flat_pred[i])
        

#%%
        
def visualisation(n):
    
    df = pd.read_csv('/content/database.csv') #.sample(5000).reset_index(drop=True)

    del df['Unnamed: 0']

    df = df[df['Sentiment'] != 'Neutre']

    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                              'Négatif':0})

    
    y_test = df['Sentiment'][:n]
    
    X_test = df['Avis']
    
    y_pred = []
    
    for i in range(n):
        
        y_pred.append(test([X_test.iloc[i]]))
        
    y_pred = pd.Series(y_pred)

    y_test = y_test[:503]

    matrice_confusion = confusion_matrix(y_test, y_pred)

    df_cm = pd.DataFrame(matrice_confusion, range(0,2), range(0,2))

    plt.figure(figsize = (10,7))
        
    sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

    plt.savefig('mactrice_BERT', dpi = 400)
        
    print('La matrice de confusion a bien été enregistrée !')
    
    print(classification_report(y_true=y_test, y_pred=y_pred))
        
        
        
        

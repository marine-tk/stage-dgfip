# Dependencies
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import sys
import numpy as np
import torch
from keras_preprocessing.sequence import pad_sequences
from transformers import CamembertTokenizer
from transformers import *
import pickle
import io

class CPU_Unpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'torch.storage' and name == '_load_from_bytes':
                return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
            else: return super().find_class(module, name)

def predict_bert(str_pred):
    f = open("model_bert.pkl",'rb')
    lr = CPU_Unpickler(f).load()

    data = [str_pred, "excellente idée"]
    query = pd.DataFrame(data, columns=['Avis'])
    
    sentences = list(query['Avis'])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Encode the comments
    tokenizer = CamembertTokenizer.from_pretrained('camembert-base',do_lower_case=True)         
    tokenized_comments_ids = [tokenizer.encode(sentence,add_special_tokens=True,max_length=128,truncation=True) for sentence in sentences]
    
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
    prediction = []   

# Importation des librairies
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import sys
import numpy as np
import torch
from keras_preprocessing.sequence import pad_sequences
from transformers import CamembertTokenizer
import pickle
import io

# Définition de l'API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def predict():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.DataFrame(json_)
            
            sentences = list(query['Avis'])
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
           
            # Encodage BERT
            tokenizer = CamembertTokenizer.from_pretrained('camembert-base',do_lower_case=True)         
            tokenized_comments_ids = [tokenizer.encode(sentence,add_special_tokens=True,max_length=128,truncation=True) for sentence in sentences]
            tokenized_comments_ids = pad_sequences(tokenized_comments_ids, maxlen=128, dtype="long", truncating="post", padding="post")
            attention_masks = []
           
            for seq in tokenized_comments_ids:
                seq_mask = [float(i>0) for i in seq]    
                attention_masks.append(seq_mask)
               
            # Prédiction
            prediction_inputs = torch.tensor(tokenized_comments_ids)          
            prediction_masks = torch.tensor(attention_masks)      
            prediction = []
           
            with torch.no_grad():

                outputs =  lr(prediction_inputs.to(device),token_type_ids=None, attention_mask=prediction_masks.to(device))               
                logits = outputs[0]               
                logits = logits.detach().cpu().numpy()               
                prediction.extend(np.argmax(logits, axis=1).flatten())  
                
            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345
        
    # La création de cette classe permettait de résoudre une erreur due à l'importation
    # du modèle 'model.pkl'
    class CPU_Unpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == 'torch.storage' and name == '_load_from_bytes':
                return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
            else: return super().find_class(module, name)

    f = open("model_bert.pkl",'rb') # le modèle doit être dans le même répertoire que le code
    lr = CPU_Unpickler(f).load()
    print ('Model loaded')

    app.run(port=port, debug=True,use_reloader=False,host="0.0.0.0")

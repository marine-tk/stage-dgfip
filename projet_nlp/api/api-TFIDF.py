# Importation des librairies
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
import sys
from sklearn.pipeline import make_pipeline 
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from imblearn.over_sampling import RandomOverSampler

# Le fichier model_tfidf.py est créé par nous même
# contient la création du modèle TF-IDF
from model_tfidf import reglog

# Définition de l'API
app = Flask(__name__)

# Permet de garder les mêmes poids et le même dictionnaire TF-IDF
# pour l'embedding de la phrase à prédire
X_train = reglog()

# Création de l'API
@app.route('/predict', methods=['POST'])

def predict():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.DataFrame(json_)

            # Embedding (TF-IDF) de la phrase à prédire
            pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
            pipe.fit(X_train['Avis'])
            query = pipe.transform(query['Avis'])
            
            # Prédiction de la régression logistique de TF-IDF
            prediction = list(lr.predict(query))

            return jsonify({'prediction': str(prediction)})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 12345

    lr = joblib.load("model_tfidf.pkl") # le modèle doit être dans le même répertoire que le code
    print ('Modèle téléchargé')

    app.run(port=port, debug=True,use_reloader=False,host="0.0.0.0")

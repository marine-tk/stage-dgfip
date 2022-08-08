# Importation des libraries
from flask import Flask, request, jsonify
import traceback
import pandas as pd
import sys
from model import fonction
import fasttext

# Création de l'application
app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def predict():
    if lr:
        try:
            json_ = request.json
            print(json_)
            query = pd.DataFrame(json_)
            prediction = []
            for index,avis_sentiment in query.iterrows() :
                prediction.append(lr.predict(avis_sentiment.Avis)[0])

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

    lr = fasttext.load_model("model_fasttext.pkl") # le modèle doit être dans le même répertoire que le code
    print ('Modèle téléchargé')

    app.run(port=port, debug=True,use_reloader=False,host="0.0.0.0")

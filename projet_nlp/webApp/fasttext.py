# Importation des librairies
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
import joblib

def predict_fasttext(str_pred):
    lr = fastText.load_model("model_fasttext.pkl")
    str_pred = str_pred
    data = [str_pred, "phrase test nécessaire"]
    query = pd.DataFrame(data, columns=['Avis'])

    prediction = []
    for index,avis_sentiment in query.iterrows() :
        prediction.append(lr.predict(avis_sentiment.Avis)[0])

    prediction = list(prediction[0])

    if prediction[0] == "__label__negatif":
        prediction[0] = 'negatif'
    if prediction[0] == "__label__positif":
        prediction[0] = 'positif'
        
     return prediction[0]

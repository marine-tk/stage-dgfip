# Import dependencies
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import make_pipeline
from imblearn.over_sampling import RandomOverSampler

def fonction() :
    
    df = pd.read_csv('scrapping_avis_all.csv')
    df = df[df['Sentiment'] != 'Neutre']
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,'Négatif':0})
    
    if len(df) !=  0:    
         X_train, X_test, y_train, y_test = train_test_split(df[["Avis"]], df['Sentiment'], test_size=0.2)
    
    # Resampling
    ros = RandomOverSampler(random_state=0)
    X_train, y_train = ros.fit_resample(X_train, y_train)
    
    df_train_resampled = pd.DataFrame()
    df_train_resampled["Avis"] = X_train
    df_train_resampled["Sentiment"] = y_train
    
    df_test = pd.DataFrame()
    df_test["Avis"] = X_test
    df_test["Sentiment"] = y_test
    
    # TF-IDF embedding
    pipe = make_pipeline(CountVectorizer(), TfidfTransformer())
    pipe.fit(X_train['Avis'])

    ## Transforme nos données textuelles en matrice TFIDF.
    feat_train = pipe.transform(X_train['Avis'])

    feat_test = pipe.transform(X_test['Avis'])

    ## Logistic Regression classifier
    lr = LogisticRegression(penalty = 'l2', dual = False, C = 10, class_weight = None,max_iter = 100,solver = 'newton-cg')
    
    ## Entraine notre modèle
    lr.fit(feat_train, y_train)
    
    # Save your model
    joblib.dump(lr, 'model_reglog.pkl')
    print("Model dumped!")
    
    # Load the model that you just saved
    lr = joblib.load('model_reglog.pkl')
    
    # Saving the data columns from training
    model_columns = list(X_train.columns)
    joblib.dump(model_columns, 'model_columns_reglog.pkl')
    print("Models columns dumped!")
    
    return X_train

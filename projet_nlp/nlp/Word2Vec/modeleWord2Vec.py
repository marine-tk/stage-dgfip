## Importation des librairies

import pandas as pd 

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import GradientBoostingClassifier

from sklearn.neural_network import MLPClassifier

from sklearn.svm import SVC

from sklearn.metrics import confusion_matrix, classification_report, roc_curve

from sklearn.model_selection import GridSearchCV

from imblearn.over_sampling import SMOTE

import matplotlib.pyplot as plt

import seaborn as sn

### À modifier selon l'environnement d'exécution
path = '/Users/geoffroyperonne/Desktop/DGFiP/Projet Analyse tweet/NLP/Représentation Word2Vec/Données/'

## Modèle Random Forest

def modele_random_forest():
    
    df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
    
    ## Importation du modèle
    clf = RandomForestClassifier(class_weight={0 : 1 , 1 : 1.3},
                       max_depth=100,
                       min_samples_split=4,
                       n_estimators=100)

    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment = sm.fit_resample(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

    ## Entraine notre modèle
    clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
    
    pred = clf.predict(dfTest[dfTest.columns[:-1]])
    
    matrice_confusion = confusion_matrix(dfTest.Sentiment, pred)
    
    
    return(matrice_confusion,clf.score(dfTest[dfTest.columns[:-1]], dfTest.Sentiment),dfTest.Sentiment,pred)



## Modèle Régression Logistique

def modele_logistic_regression():
    
    df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
    
    df = df[df['Sentiment'] != 'Neutre']
    
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                             'Négatif':0})


    dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
    
    ## Importation du modèle
    clf = LogisticRegression(penalty = 'l1', dual = False, C = 100, 
                             class_weight = {0 : 1 , 1 : 1.3}, max_iter = 1000, solver='liblinear')
    
    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment = sm.fit_resample(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

    ## Entraine notre modèle
    clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
    
    pred = clf.predict(dfTest[dfTest.columns[:-1]])
    
    matrice_confusion = confusion_matrix(dfTest.Sentiment, pred)
    
    
    return(matrice_confusion,clf.score(dfTest[dfTest.columns[:-1]], dfTest.Sentiment),dfTest.Sentiment,pred)


## Modèle Gradient Boosting

def modele_gradient_boosting():
    
    df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
 
    df = df[df['Sentiment'] != 'Neutre']
 
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                           'Négatif':0})


    dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
 
    ## Importation du modèle
    clf = GradientBoostingClassifier(n_estimators =  7, max_depth = 7, min_samples_split =  5)
    
    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment = sm.fit_resample(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

    ## Entraine notre modèle
    clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
    
    pred = clf.predict(dfTest[dfTest.columns[:-1]])
    
    matrice_confusion = confusion_matrix(dfTest.Sentiment, pred)
    
    
    return(matrice_confusion,clf.score(dfTest[dfTest.columns[:-1]], dfTest.Sentiment),dfTest.Sentiment,pred)

## Modèle de réseaux de neuronnes

def modele_neural_network():
    
    df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
 
    df = df[df['Sentiment'] != 'Neutre']
 
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                           'Négatif':0})


    dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
 
    ## Importation du modèle
    clf = MLPClassifier(solver='adam', alpha=0.001, activation='relu', learning_rate_init=0.00001,
                    hidden_layer_sizes=(150,))
    
    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment = sm.fit_resample(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)

    ## Entraine notre modèle
    clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
    
    pred = clf.predict(dfTest[dfTest.columns[:-1]])
    
    matrice_confusion = confusion_matrix(dfTest.Sentiment, pred)
    
    
    return(matrice_confusion,clf.score(dfTest[dfTest.columns[:-1]], dfTest.Sentiment),dfTest.Sentiment,pred)


def modele_SVC():
    
    df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
 
    df = df[df['Sentiment'] != 'Neutre']
 
    df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                           'Négatif':0})


    dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
 
    ## Importation du modèle
    clf = SVC(kernel='rbf', C=100000, class_weight = {0 : 1 , 1 : 2.9}, gamma=0.0001)
    
    sm = SMOTE(k_neighbors=3, sampling_strategy=0.75)
    
    dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment = sm.fit_resample(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)


    ## Entraine notre modèle
    clf.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
    
    pred = clf.predict(dfTest[dfTest.columns[:-1]])
    
    matrice_confusion = confusion_matrix(dfTest.Sentiment, pred)
    
    
    return(matrice_confusion,clf.score(dfTest[dfTest.columns[:-1]], dfTest.Sentiment),dfTest.Sentiment,pred)



    
def representation(modele):
    
    if modele == 'tree':
        
        matrice , score , y_test , y_pred = modele_random_forest()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_tree_Word2Vec', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
                
    
    if modele == 'regression logistique':
        
        matrice , score , y_test , y_pred = modele_logistic_regression()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_logit_reg_Word2Vec', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
        
    if modele == 'gradient':
        
        matrice , score , y_test , y_pred = modele_gradient_boosting()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_gradient_boosting_Word2Vec', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
        
    if modele == 'neuronne':
        
        matrice , score , y_test , y_pred = modele_neural_network()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_reseau_neuronne_Word2Vec', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
    if modele == 'SVC':
        
        matrice , score , y_test , y_pred = modele_SVC()
        
        df_cm = pd.DataFrame(matrice, range(0,2), range(0,2))
        
        plt.figure(figsize = (10,7))
        
        sn.heatmap(df_cm, annot=True, cmap="BuPu" , linewidths=5, fmt="d", annot_kws={'size': 23})

        plt.savefig('mactrice_confusion_SVC_Word2Vec', dpi = 400)
        
        print('La matrice de confusion a bien été enregistrée !')
    
        print(classification_report(y_true=y_test, y_pred=y_pred))
        
        
        
        
def best_parameters(modele):
    
    if modele == 'tree':
    
        df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
            
        ## Création de la GridSearch
        n_estimators =  [50, 100]
        max_depth = [50,100]
        min_samples_split=[3,4]
        
        
        param_grid = {'min_samples_split' : min_samples_split,
                      'max_depth': max_depth,
                      'n_estimators': n_estimators}
        
        grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv = 2, return_train_score=True, verbose = 3, scoring='f1_macro')
        
        grid_search.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
        
        print("Best estimator:\n{}".format(grid_search.best_estimator_))


    if modele == 'regression logistique':
    
        df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
            
        ## Création de la GridSearch
        max_iter =  [400, 600]
        class_weight = [None, 'balanced']
        C = [ 1, 10, 100]
        penalty = ['l1', 'l2']
        solver = ['newton-cg', 'liblinear']
        
        
        param_grid = {'max_iter' : max_iter,
                      'class_weight': class_weight,
                      'C': C,
                      'penalty': penalty,
                      'solver': solver}
        
        grid_search = GridSearchCV(LogisticRegression(), param_grid, cv = 2, return_train_score=True, verbose = 3, scoring='f1_macro')
        
        grid_search.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
        
        print("Best estimator:\n{}".format(grid_search.best_estimator_))
        
        
        
    if modele == 'gradient':
    
        df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
            
        ## Création de la GridSearch
        n_estimators =  [7,8]
        max_depth = [7, 8]
        min_samples_split = [2, 4]
        
        
        param_grid = {'n_estimators' : n_estimators,
                      'max_depth': max_depth,
                      'min_samples_split' : min_samples_split}
        
        grid_search = GridSearchCV(GradientBoostingClassifier(), param_grid, cv = 2, return_train_score=True, verbose = 3, scoring='f1_macro')
        
        grid_search.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
        
        print("Best estimator:\n{}".format(grid_search.best_estimator_))


    if modele == 'neuronne':
    
        df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
            
        ## Création de la GridSearch
        solver =  ['adam']
        alpha = [ 0.001]
        hiden_layer_sizes = [(150,)]
        
        param_grid = {'solver' : solver,
                      'alpha': alpha, 
                      'hiden_layer_sizes': hiden_layer_sizes}
        
        grid_search = GridSearchCV(MLPClassifier(), param_grid, cv = 2, return_train_score=True, verbose = 3, scoring='f1_macro')
        
        grid_search.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
        
        print("Best estimator:\n{}".format(grid_search.best_estimator_))

    
    if modele == 'SVC':
    
        df = pd.read_csv(path+'Encodage_Word2Vec(300d).csv')
            
        df = df[df['Sentiment'] != 'Neutre']
            
        df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                                               'Négatif':0})

        dfTrain, dfTest = train_test_split(df, train_size=0.8, stratify=df.Sentiment)
            
        ## Création de la GridSearch
        C =  [1000, 10000, 100000]
        gamma = [0.0001, 0.001]
        
        param_grid = {'C' : C,
                      'gamma': gamma}
        
        grid_search = GridSearchCV(SVC(), param_grid, cv = 2, return_train_score=True, verbose = 3, scoring='f1_macro')
        
        grid_search.fit(dfTrain[dfTrain.columns[:-1]], dfTrain.Sentiment)
        
        print("Best estimator:\n{}".format(grid_search.best_estimator_))
        

def plot_roc_curve(fper_rf, tper_rf, fper_rl, tper_rl, fper_nn, tper_nn, fper_gb, tper_gb, fper_svc, tper_svc):
    
    fig, ax = plt.subplots(figsize=(14,8))
    
    sn.lineplot([0,1], [0,1], ax=ax, color="darkslategray")
    
    sn.lineplot(fper_rf, tper_rf, ax=ax, color="darkcyan")
    
    sn.lineplot(fper_rl, tper_rl, ax=ax)
    
    sn.lineplot(fper_nn, tper_nn, ax=ax, color="darkmagenta")
    
    sn.lineplot(fper_gb, tper_gb, ax=ax, color="seagreen")
    
    sn.lineplot(fper_svc, tper_svc, ax=ax, color="mediumvioletred")
    
    ax.set_xlabel( "Taux de faux positifs" , size = 15 ) 
    
    ax.set_ylabel( "Taux de vrais positifs" , size = 15 ) 
    
    ax.legend(['Classifieur aléatoire','Random Forest','Régression Logistique','Neural Networks','Gradient Boosting','SVC'], facecolor='w')
    
    sn.set_style('darkgrid')
    
    plt.savefig('Courbe_ROC_Word2Vec', dpi = 400)
    



def roc_curves():
    
    ## Random Forest

    matrice , score , y_test , y_pred = modele_random_forest()
    
    fper_rf, tper_rf, thresholds = roc_curve(y_test, y_pred)
    
    ## Regression Logistique
    
    matrice , score , y_test , y_pred = modele_logistic_regression()
    
    fper_rl, tper_rl, thresholds = roc_curve(y_test, y_pred)    

    ## Réseaux de neuronnes
    
    matrice , score , y_test , y_pred = modele_neural_network()
    
    fper_nn, tper_nn, thresholds = roc_curve(y_test, y_pred)  
    
    ## Gradient Boosting
    
    matrice , score , y_test , y_pred = modele_gradient_boosting()
    
    fper_gb, tper_gb, thresholds = roc_curve(y_test, y_pred)
    
    ## SVC
    
    matrice , score , y_test , y_pred = modele_gradient_boosting()
    
    fper_svc, tper_svec, thresholds = roc_curve(y_test, y_pred) 
    
    
    plot_roc_curve(fper_rf, tper_rf, fper_rl, tper_rl, fper_nn, tper_nn, fper_gb, tper_gb, fper_svc, tper_svec) 
    
    



    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        

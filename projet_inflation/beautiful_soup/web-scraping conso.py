from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime
import statistics as stat
import time

def clean(str) :
  ''' Pour nettoyer le prix (qui est un string) et le convertir en flottant'''
  str = str.replace(' ','')
  str = str.replace('\n','')
  str = str.replace('€/L','')
  str = str.replace('€/U','')
  str = str.replace(',','.')
  str = str.replace('€/KG','')
  str = str.replace('€','')
  return float(str)

def extract_tabacco():
    ## Extraction des prix des cartouches de cigarettes
    html_text = requests.get("https://fumermoinscher.com/categorie-produit/cigarettes/?orderby=popularity", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
    soup = BeautifulSoup(html_text, 'html.parser')
    cig_cartouche = []
    for cig in soup.find_all('bdi'):
        try :
            cig_cartouche.append(float(clean(cig.get_text())))
        except :
            pass

    ## Extraction des prix des tabacs à rouler
    time.sleep(2)
    html_text = requests.get("https://fumermoinscher.com/categorie-produit/tabac/?orderby=popularity", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
    soup = BeautifulSoup(html_text, 'html.parser')
    cig_roll1 = []
    cig_roll2 = []
    for cig in soup.find_all('bdi'):
        try :
            cig_roll1.append(float(clean(cig.get_text())))
        except :
            pass

    for i in range(len(cig_roll1)):
        if i % 2 == 1:
            cig_roll2.append(cig_roll1[i])

    product , mean_price = ['Cartouche (20 paquets)' , 'Tabac à rouler (500g)'] , [round(stat.mean(cig_cartouche) , 2) , round(stat.mean(cig_roll2) , 2)]

    return(pd.DataFrame(list(zip([mean_price[0]] , [mean_price[1]])) , index = ['prix moyen'], columns = product).T)

def extract_household_tasks():

    ## Extraction des lessives (€/L)

    sites = ['https://www.carrefour.fr/p/lessive-savon-de-marseille-carrefour-essential-3560071238025',
             'https://www.carrefour.fr/p/lessive-liquide-simpl-3560071241896',
             'https://www.carrefour.fr/p/lessive-liquide-famille-et-bebe-l-arbre-vert-3450601031793',
             'https://www.carrefour.fr/p/lessive-liquide-total-x-tra-3178041332293',
             'https://www.carrefour.fr/p/lessive-liquide-au-savon-noir-briochin-3383482304468',
             'https://www.carrefour.fr/p/lessive-liquide-adoucissant-minidou-2en1-x-tra-3178041331920']

    lessive = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')
        time.sleep(3)
        
        try :
            lessive.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1
            
        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des lessives' )
    
    ## Extraction nettoyant vitre (€/L)
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/nettoyant-vitres-3en1-carrefour-expert-3560070241293',
             'https://www.carrefour.fr/p/nettoyant-vitres-3en1-carrefour-3560070241385',
             'https://www.carrefour.fr/p/nettoyant-menager-vitres-triple-action-ajax-8714789750514',
             'https://www.carrefour.fr/p/nettoyant-menager-lave-vitres-carrefour-eco-planet-3560070829521',
             'https://www.carrefour.fr/p/nettoyant-vitres-cristal-sans-traces-ajax-8718951340442',
             'https://www.carrefour.fr/p/nettoyant-vitres-ecologique-rainett-4009175165190']

    vitre = []

    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')
        time.sleep(3)

        try :
            vitre.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des produits pour vitres' )

    ## Extraction papier toilette (€/U)
   
    time.sleep(2)

    sites = ['https://www.carrefour.fr/p/papier-toilette-confort-lotus-7322540835380?t=2617',
             'https://www.carrefour.fr/p/papier-toilette-confort-doux-carrefour-3560070332557?t=2617',
             'https://www.carrefour.fr/p/papier-toilette-blanc-dayly-8004260496810?t=2617',
             'https://www.carrefour.fr/p/papier-toilette-just-one-5-epaisseurs-aqua-tube-lotus-7322540818796?t=2617']

    WC = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')  
        time.sleep(3)

        try :
            WC.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des papiers toilettes' )   

    ## Extraction éponges (€/U)
   
    time.sleep(2)

    sites = ['https://www.carrefour.fr/p/eponges-vaisselle-carrefour-expert-3560070215218',
             'https://www.carrefour.fr/p/eponges-multi-surfaces-super-absorbantes-carrefour-expert-3560070759163',
             'https://www.carrefour.fr/p/eponges-grattantes-super-efficaces-spontex-3011261030962',
             'https://www.carrefour.fr/p/eponges-vegetales-rozenbal-3142761400037',
             'https://www.carrefour.fr/p/eponges-gratton-vert-scotch-brite-3134373600028',
             'https://www.carrefour.fr/p/eponge-grattante-splendelli-8008990127112']

    eponge = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')      
        time.sleep(3)

        try :
            eponge.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des éponges' )
              
    product , mean_price = ['Lessive (€/L)' , 'Nettoyant vitre (€/L)' , 
                            'Papier toilette (€/U)' , 'Eponge (€/U)'] , [round(stat.mean(lessive) , 2) , 
                                                                         round(stat.mean(vitre) , 2) , round(stat.mean(WC) , 2) , 
                                                                         round(stat.mean(eponge) , 2)]       

    return(pd.DataFrame(list(zip([mean_price[0]] , [mean_price[1]] , [mean_price[2]] , [mean_price[3]])) , index = ['prix moyen'], columns = product).T)
 

def extract_hygiene():

    ## Extraction des gels douche (€/L)
   
    time.sleep(2)

    sites = ['https://www.carrefour.fr/p/gel-douche-fleur-de-cerisier-le-petit-marseillais-3574661550510?t=2421',
             'https://www.carrefour.fr/p/gel-douche-creme-surgras-so-bio-etic-3517360012750?t=2421',
             'https://www.carrefour.fr/p/gel-douche-amande-douce-carrefour-soft-3560071254988?t=2421',
             'https://www.carrefour.fr/p/gel-douche-creme-surgras-beurre-de-karite-vendome-3346029200241?t=2421',
             'https://www.carrefour.fr/p/creme-de-douche-soin-nutrition-intense-dove-8712561594424?t=2421',
             'https://www.carrefour.fr/p/gel-douche-grenade-ushuaia-3600551033686?t=2421',             'https://www.carrefour.fr/p/gel-douche-biome-protection-dermo-peau-sensible-sanex-8718951391901?t=2421',
             'https://www.carrefour.fr/p/dentifrice-soin-complet-sensodyne-5054563109620?t=2448',
             'https://www.carrefour.fr/p/dentifrice-triple-protection-menthe-fraiche-aquafresh-5054563098870?t=2448',
             'https://www.carrefour.fr/p/dentifrice-blancheur-bi-fluore-fluocaril-8720182015464?t=2448']

    savon = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')   
        time.sleep(3)

        try :
            savon.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des gels douche' )
      

    ## Extraction dentifrice (€/L)
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/dentifrice-pro-sensitive-gencive-purifie-nettoyage-intense-oral-b-8006540344095',
             'https://www.carrefour.fr/p/dentifrice-kids-fraise-bio-signal-8710604788823?t=2448',
             'https://www.carrefour.fr/p/dentifrice-haleine-pure-signal-3014230002601?t=2448',
             'https://www.carrefour.fr/p/dentifrice-tonigencyl-capital-gencives-colgate-8718951015418?t=2448']
    dentifrice = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')      
        time.sleep(3)

        try :
            dentifrice.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des dentifrices' )
     

    ## Extraction tampons (€/U)
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/tampons-hygenique-original-super-plus-x24-nett-3574661350868',
             'https://www.carrefour.fr/p/tampons-compak-pearl-regulier-avec-applicateur-x18-tampax-4015400690252',
             'https://www.carrefour.fr/p/tampons-pure-super-avec-applicateur-carrefour-soft-3560071402853',]
    tampons = []
    resultat =0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')       
        time.sleep(3)

        try :
            tampons.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass


    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des protections hygiéniques' )

   
    ## Extraction préservatifs (€/U)
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/preservatif-classique-jeans-durex-3059948002611',
             'https://www.carrefour.fr/p/preservatif-nude-peau-contre-peau-ultra-fin-original-durex-3059948002949']
    preservatifs = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')     
        time.sleep(3)

        try :
            preservatifs.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
            resultat += 1

        except :
            pass

    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des préservatifs' )
 
    product , mean_price = ['Gel douche (€/L)' , 'Dentifrice (€/L)' , 
                            'Protection hygiénique (€/U)' , 'Préservatifs (€/U)'] , [round(stat.mean(savon) , 2) ,
                                                                                     round(stat.mean(dentifrice) , 2) , 
                                                                                     round(stat.mean(tampons) , 2) , 
                                                                                     round(stat.mean(preservatifs) , 2)]
      
    return(pd.DataFrame(list(zip([mean_price[0]] , [mean_price[1]] , [mean_price[2]] , [mean_price[3]])) , index = ['prix moyen'], columns = product).T)

def extract_food():
 
    ## Extraction pates

    sites = ["https://www.carrefour.fr/p/pates-coquillettes-carrefour-3560070328918",
             "https://www.carrefour.fr/p/pates-fusilli-carrefour-3560070329038",
             "https://www.carrefour.fr/p/pates-spaghetti-carrefour-3560070328888",
             "https://www.carrefour.fr/p/pates-torti-panzani-3038350013606",
             "https://www.carrefour.fr/p/pates-farfalle-panzani-3038350269805",
             "https://www.carrefour.fr/p/pates-macaroni-carrefour-3560070329151",
             "https://www.carrefour.fr/p/pates-penne-rigate-carrefour-3560070555390",
             "https://www.carrefour.fr/p/pates-coudes-rayes-panzani-3038350013507"]
    pate = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')  
        
        time.sleep(3)
        try:
          pate.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1
          
        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL des pâtes")
       
    ## Extraction eau
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/eau-minerale-naturelle-abatilles-3048431061990",
             "https://www.carrefour.fr/p/eau-minerale-naturel-biovive-3274082058786",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-minerale-naturelle-contrex-7613035866393",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-volvic-3057640257858",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-courmayeur-8024884501400",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-des-alpes-carrefour-classic-3245414228900",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-carrefour-3245414469433",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-evian-3068320120263",
             "https://www.carrefour.fr/p/eau-minerale-naturelle-carrefour-classic-3270190178095"]
    eau = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')  
        time.sleep(3)

        try:
          eau.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour l'eau")

    ## Extraction nutella
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/pate-a-tartiner-noisettes-cacao-nutella-3017620422003",
                 "https://www.carrefour.fr/p/pate-a-tartiner-au-cacao-noisettes-milka-7622201515492",
                 "https://www.carrefour.fr/p/pate-a-tartiner-noisette-et-cacao-bonne-maman-3608580065340",
                 "https://www.carrefour.fr/p/pate-a-tartiner-noisette-cacao-lucien-georgelin-3330720237361",
                 "https://www.carrefour.fr/p/pate-a-tartiner-au-cacao-noisettes-carrefour-classic-3560071005641"]
    nutella = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')     
        time.sleep(3)

        try:
          nutella.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL de pâte à tartiner")

    ## Extraction riz
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/riz-long-grain-10-min-ben-s-original-5410673005052",
             "https://www.carrefour.fr/p/riz-bio-long-grain-carrefour-bio-3560071230654",
             "https://www.carrefour.fr/p/riz-long-de-camargue-complet-etuve-igp-reflets-de-france-3560070828821",
             "https://www.carrefour.fr/p/riz-long-grain-10mn-carrefour-3560070822270",
             "https://www.carrefour.fr/p/riz-long-grain-incollable-5mn-lustucru-3038354524108"]

    riz = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')    
        time.sleep(3)

        try:
          riz.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour le riz")
    

    ## Extraction poulet
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/filets-de-poulet-5413458017578",
                "https://www.carrefour.fr/p/filets-de-poulet-5413458060185",
                "https://www.carrefour.fr/p/filets-de-poulet-tranche-5413458061427",
                "https://www.carrefour.fr/p/filets-de-poulet-en-lanieres-5413458066880"]
    poulet = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')    
        time.sleep(3)

        try:
          poulet.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour le poulet")    

    ## Extraction boeuf
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/viande-hachee-pur-boeuf-5-mg-carrefour-le-marche-3245415074230",
               "https://www.carrefour.fr/p/viande-bovine-steak-hache-special-burger-15-mg-dabia-3039050338792",
               "https://www.carrefour.fr/p/steak-hache-viande-bovine-race-salers-reflets-de-france-3245415449960",
               "https://www.carrefour.fr/p/steaks-haches-viande-bovine-race-aubrac-reflets-de-france-3245415449953",
               "https://www.carrefour.fr/p/steak-hache-pur-boeuf-5-mg-carrefour-bio-3245415327282"]

    boeuf = []
    resultat = 0


    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')   
        time.sleep(3)

        try:
          boeuf.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère", (resultat/len(sites))*100,"% des URL pour le boeuf")
      

    ## Extraction carottes
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/carottes-bio-carrefour-bio-3270190010074',
             'https://www.carrefour.fr/p/carottes-petit-prix-3276550261162',
             'https://www.carrefour.fr/p/carottes-botte-fanes-3276556001885',
             'https://www.carrefour.fr/p/carottes-petit-prix-3276550261162',
             'https://www.carrefour.fr/p/carottes-planete-vegetal-3523680244535']
    carottes = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')     
        time.sleep(3)

        try:
          carottes.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour les carottes")


    ## Extraction pommes
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/pommes-gala-royal-gala-3276554937087',
             'https://www.carrefour.fr/p/pommes-golden-delicious-vrac-filiere-qualite-carrefour-3276552247867',
             'https://www.carrefour.fr/p/pommes-golden-delicious-3276554835079',
             'https://www.carrefour.fr/p/pommes-jonagold-bicolore-3276550165774',
             'https://www.carrefour.fr/p/pommes-granny-smith-vrac-3276554965424',
             'https://www.carrefour.fr/p/pommes-gala-bio-carrefour-bio-3276550063650']
    pommes = []
    resultat = 0
    
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')    
        time.sleep(3)

        try:
          pommes.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour les pommes")

    ## Extraction oeuf
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/pommes-gala-royal-gala-3276554937087',
             'https://www.carrefour.fr/p/pommes-golden-delicious-vrac-filiere-qualite-carrefour-3276552247867',
             'https://www.carrefour.fr/p/pommes-golden-delicious-3276554835079',
             'https://www.carrefour.fr/p/pommes-jonagold-bicolore-3276550165774',
             'https://www.carrefour.fr/p/pommes-granny-smith-vrac-3276554965424']
    oeufs = []
    resultat = 0
    
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')    
        time.sleep(3)

        try:
          oeufs.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour les oeufs")  

    ## Extraction beurre
   
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/beurre-doux-gastronomique-president-3155251205500',
             'https://www.carrefour.fr/p/beurre-doux-tendre-president-3155251205524',
             'https://www.carrefour.fr/p/beurre-gastronomique-doux-carrefour-classic-3245411900458',
             'https://www.carrefour.fr/p/beurre-doux-moule-paysan-breton-3412290015980',
             'https://www.carrefour.fr/p/beurre-demi-sel-tendre-elle-vire-3451790988813']
    beurre = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')     
        time.sleep(3)

        try:
          beurre.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour le beurre")


    ## Extraction saumon
   
    time.sleep(2)

    sites = ["https://www.carrefour.fr/p/saumon-fume-simpl-3560071435394",
             "https://www.carrefour.fr/p/paves-de-saumon-avec-peau-sans-aretes-filiere-qualite-carrefour-3523680308848",
             "https://www.carrefour.fr/p/filet-de-saumon-asc-filiere-qualite-carrefour-3523680145948",
             "https://www.carrefour.fr/p/darne-de-saumon-fqc-asc-3276558794877",
             "https://www.carrefour.fr/p/paves-de-saumon-avec-peau-sans-aretes-filiere-qualite-carrefour-3523680308831",
             "https://www.carrefour.fr/p/pave-de-saumon-asc-filiere-qualite-carrefour-3276558790824"]

    saumon = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')
  
        time.sleep(3)

        try:
          saumon.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour le saumon")


    ## Extraction crevette
   
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/crevettes-cuites-30-50-asc-3276550100256",
             "https://www.carrefour.fr/p/crevettes-entieres-cuites-delpierre-3276550315766",
             "https://www.carrefour.fr/p/crevettes-grises-cuites-jumbo-3000000111659",
             "https://www.carrefour.fr/p/crevettes-cuites-40-60-asc-fqc-3000000111789",
             "https://www.carrefour.fr/p/crevettes-entieres-cuites-asc-delpierre-3336370035142",
             "https://www.carrefour.fr/p/crevettes-rouges-d-argentine-marnatura-8436042352272"]
    crevette = []
    resultat = 0

    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')   
        time.sleep(3)

        try:
          crevette.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1

        except:
          pass

    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour les crevettes")

    ## Extraction baguette 
    time.sleep(2)
    sites = ["https://www.carrefour.fr/p/baguettes-campagnardes-filiere-qualite-carrefour-3276550272410",
             "https://www.carrefour.fr/p/baguette-campagnarde-filiere-qualite-carrefour-3276550350613",
             "https://www.carrefour.fr/p/baguettes-rustiques-3276550272403",
             "https://www.carrefour.fr/p/baguette-a-l-epeautre-filiere-qualite-carrefour-3523680330139",
             "https://www.carrefour.fr/p/baguettes-3276550350606",
             "https://www.carrefour.fr/p/baguette-carrefour-3276551080656",
             "https://www.carrefour.fr/p/baguette-rustique-carrefour-3276559526460",
             "https://www.carrefour.fr/p/baguette-cereales-carrefour-3276550002307",
             "https://www.carrefour.fr/p/baguette-campagnarde-filiere-qualite-carrefour-3276558853451"]
    baguette = []
    resultat = 0
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')      
        time.sleep(5)
        try:
          baguette.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1
        except:
          pass
    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour la baguette")
   
    ## Extraction ketchup 
    time.sleep(2)
    sites = ['https://www.carrefour.fr/p/ketchup-heinz-0000087157215',
             'https://www.carrefour.fr/p/ketchup-amora-8712100751370',
             'https://www.carrefour.fr/p/ketchup-tomato-simpl-3560070993000',
             'https://www.carrefour.fr/p/ketchup-carrefour-3560071121068',
             'https://www.carrefour.fr/p/ketchup-bio-heinz-8715700407760']
    ketchup = []
    resultat = 0
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')     
        time.sleep(5)
        try:
          ketchup.append(float(clean(soup.find( class_ = "ds-body-text ds-body-text--size-s" ).text)))
          resultat+=1
        except:
          pass
    print("L'algorithme considère",(resultat/len(sites))*100,"% des URL pour le ketchup")

    product , mean_price = ['Pates (€/kg)' ,    'Eau (€/kg)' ,
                            'Nutella (€/kg)' ,  'Poulet (€/kg)' ,
                            'Boeuf (€/kg)' ,    'Carottes (€/kg)' ,
                            'Pommes (€/kg)' ,   'Oeufs (€/kg)' ,
                            'Beurre (€/kg)' ,   'Saumon (€/kg)',
                            'Crevette (€/kg)',  'Baguette (€/kg)',                       
                            'Ketchup (€/kg)'] , [round(stat.mean(pate) , 2) , round(stat.mean(eau) , 2) ,
                             round(stat.mean(nutella) , 2) , round(stat.mean(poulet) , 2) ,
                             round(stat.mean(boeuf) , 2) , round(stat.mean(carottes) , 2) ,
                             round(stat.mean(pommes) , 2) , round(stat.mean(oeufs) , 2),
                             round(stat.mean(beurre) , 2), round(stat.mean(saumon) , 2),
                             round(stat.mean(crevette) , 2), round(stat.mean(baguette) , 2),                            
                             round(stat.mean(ketchup) , 2)]   

    return(pd.DataFrame(list(zip([mean_price[0]], [mean_price[1]] ,
                                 [mean_price[2]] , [mean_price[3]] ,
                                 [mean_price[4]] , [mean_price[5]] ,
                                 [mean_price[6]], [mean_price[7]],
                                 [mean_price[8]], [mean_price[9]],
                                 [mean_price[10]], [mean_price[11]],                                
                                 [mean_price[12]])) , index = ['prix moyen'], columns = product).T)


def extract_medecine():
   
    ## Extraction du paracetamol (boîte de 8 comprimés de 1000mg)
    sites = ['https://lasante.net/nos-medicaments/douleurs-et-fievres/paracetamol/doliprane-1000-mg-comprimes-x-8.html',                        
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/paracetamol/paracetamol-mylan-1000-mg-comprimes-x-8.html',                          
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/paracetamol/dafalgan-1-g-comprimes-x-8.html',                        
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/paracetamol/efferalgan-1-g-comprimes-effervescents-x-8.html']
    paracetamol = []
    resultat = 0
    for url in sites:      
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')             
        time.sleep(3)
        try :          
            paracetamol.append(float(clean(soup.find( class_ = "produit__price" ).text)))

            resultat += 1
        except :          
            pass
    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL du paracétamol' )
   
    ## Extraction du ibuprofène (boîte de 12 comprimés de 400mg)   
    time.sleep(2)
    sites = ['https://lasante.net/nos-medicaments/douleurs-et-fievres/ibuprofene/nurofenflash-400-mg-x-12.html',          
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/ibuprofene-mylan-400-mg-lysinate-d-ibuprofene-x-12.html',            
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/ibuprofene/spedifen-400-mg-x-12.html',            
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/ibuprofene/nurofen-400-mg-x-12.html',            
             'https://lasante.net/nos-medicaments/douleurs-et-fievres/ibuprofene/iprafeine-400-mg100-mg-comprimes-x-12.html']
    ibu = []
    resultat = 0
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser')      
        time.sleep(3)
        try :
            ibu.append(float(clean(soup.find( class_ = "produit__price" ).text)))
            resultat += 1
        except :
            pass
    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL de l\'ibuprofène' )
   
    ## Extraction des désinfectants (125mL) 
    time.sleep(2)
    sites = ['https://lasante.net/nos-medicaments/medicaments-premiers-soins/antiseptiques/betadine-dermique-10-125-ml.html',    
             'https://lasante.net/nos-medicaments/medicaments-premiers-soins/antiseptiques/betadine-scrub-4-125-ml.html',           
             'https://lasante.net/nos-medicaments/medicaments-premiers-soins/antiseptiques/dakin-stabilise-125-ml.html',        
             'https://lasante.net/nos-medicaments/medicaments-premiers-soins/antiseptiques/mercryl-solution-pour-application-cutanee-125-ml.html']
    desinfect = []
    resultat = 0
    for url in sites:
        html_text = requests.get(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}).text
        soup = BeautifulSoup(html_text, 'html.parser') 
        time.sleep(3)
        try :
            desinfect.append(float(clean(soup.find( class_ = "produit__price" ).text)))
            resultat += 1
        except :
            pass
    print('L\'algorithme considère', resultat/len(sites)*100, '% des URL des desinfectants' )  
    product , mean_price = ['Paracetamol (boîte de 8 comprimés de 1000mg)' , 
                            'Ibuprofène (boîte de 12 comprimés de 400mg)' , 
                            'Désinfectants (125mL)'] , [round(stat.mean(paracetamol) , 2) , round(stat.mean(ibu) , 2) , round(stat.mean(desinfect) , 2)]
    return(pd.DataFrame(list(zip([mean_price[0]] , [mean_price[1]] , [mean_price[2]])) , index = ['prix moyen'], columns = product).T)

def concat():
    '''Permet la concaténation de tous les DataFrame créés'''
    df_tabacco = pd.DataFrame(index=["prix moyen"])
    df_tabacco["Cartouche 20 paquets"] = [57.27]
    df_tabacco["Tabac a rouler 500g"] = [86.1]
    df_tabacco = df_tabacco.T
    df = (pd.concat([ df_tabacco , extract_household_tasks() , extract_hygiene() , extract_food() , extract_medecine()])).T
    df['Date'] = [str(datetime.date.today())]
    return(df)
   

def init_df():
    '''Création du DataFrame des prix initiaux au 20 juin 2022'''
    df_init = pd.DataFrame(np.array([[57.27,86.10,2.74,2.27,0.3,0.66,17.78,40.4,0.18,0.76,3.46,0.3,8.22,7.31,13.1,1.21,1.21,1,9.28,20.19,15.92,4.19,2.53,2.02,3.85,2.91]]), columns = ['Cartouche (20 paquets)' , 'Tabac à rouler (500g)']  + ['Lessive (€/L)' , 'Nettoyant vitre (€/L)' , 'Papier toilette (€/U)' , 'Eponge (€/U)'] + ['Gel douche (€/L)' , 'Dentifrice (€/L)' , 'Protection hygiénique (€/U)' , 'Préservatifs (€/U)'] + ['Pates (€/kg)' ,    'Eau (€/kg)' , 'Nutella (€/kg)' ,  'Poulet (€/kg)' , 'Boeuf (€/kg)' ,    'Carottes (€/kg)' , 'Pommes (€/kg)' ,   'Oeufs (€/kg)' , 'Beurre (€/kg)' ,   'Saumon (€/kg)', 'Crevette (€/kg)',  'Baguette (€/kg)','Ketchup (€/kg)'] + ['Paracetamol (boîte de 8 comprimés de 1000mg)' ,'Ibuprofène (boîte de 12 comprimés de 400mg)' , 'Désinfectants (125mL)'])
    return(df_init)
 
def decomposition_prix_valeur(df_init , df):
    '''Permet la conversion en base 100 et l'enregistrement du fichier CSV'''
    new_df = df.copy()
    
    for i in range(len(df_init.T)):
         new_df.iloc[0,i] = round((df.iloc[0,i]/df_init.iloc[0,i])*100,3)
        
    df.to_csv('/home/marinetk/prix/'+'prix' + str(datetime.date.today())[:10] + '.csv')
    print('Fichier des prix CSV enregistré')
        
    new_df.to_csv('/home/marinetk/valeur_100/'+'valeur_100' + str(datetime.date.today())[:10] + '.csv')
    print('Fichier CSV enregistré')
   

def final_function():
    '''Il s'agit de la fonction qui appelle toutes les autres'''
    return(decomposition_prix_valeur(init_df(), concat()))

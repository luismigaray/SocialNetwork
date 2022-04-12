#Operaciones para la BD.
from __future__ import division
import psycopg2
import sys, nltk, re, string, heapq, gensim
from nltk.corpus   import stopwords
from psycopg2 import Error
from nltk.tokenize import TweetTokenizer
from collections   import Counter
from prettytable   import PrettyTable
from textblob      import TextBlob
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.cluster import KMeans
from gensim import corpora, models
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
import pandas.io.sql as sqlio
from optimus import Optimus

#nltk.download('stopwords')
sw = stopwords.words('spanish')
lemma = WordNetLemmatizer()
op = Optimus()

def obtenerTweets():

    try:
        
        connection = psycopg2.connect(user = "m.soto.montesinos",
                                      password = "XXXXXX",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "twitterBBVA")

        query = "select text from test"
        
        #DataFrame
        tweets = sqlio.read_sql_query(query, connection)
        
        #Array de tweets
        #cursor = connection.cursor()
        #cursor.execute(query)
        #tweets = cursor.fetchall()
        
    except (Exception, psycopg2.DatabaseError) as error :
    
        print ("Error obteniendo los datos", error)
    
    finally:
        
        #Cerramos la conexión de la base de datos.
        if (connection):
            
            #cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return tweets

def limpiarYTokenizarTweet(tweet):
    
    tweet   = re.sub(r'\$\w*', '', tweet)  # Remove tickers
    tweet   = re.sub(r'http?:.*$', '', tweet)
    tweet   = re.sub(r'https?:.*$', '', tweet)
    tweet   = re.sub(r'pic?.*\/\w*', '', tweet)
    tweet   = re.sub(r'[' + string.punctuation + ']+', ' ', tweet)  # Remove puncutations like 's
    
    tokens = TweetTokenizer(strip_handles = True, reduce_len = True).tokenize(tweet)
    tokens = [w.lower() for w in tokens if w not in sw and len(w) > 2 and w.isalpha()]
    tokens = [lemma.lemmatize(word) for word in tokens]
    
    return " ".join(tokens)

def main():

    tweets = obtenerTweets()
    cleanTweets = []
    
    for index, row in tweets.iterrows():
        
        tweet =(row['text'])
        cleanTweet = limpiarYTokenizarTweet(tweet)
        cleanTweets.append(cleanTweet)
        
    print(cleanTweets)
    

if __name__ == '__main__':
    main()


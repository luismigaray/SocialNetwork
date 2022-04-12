# FE 595
# MidTerm Project


# Required Libraries
# the request library will be used to retrieve the file from the specify URL
import requests

#for NLP textblob and different package within TextBlob
from textblob import TextBlob, Word, Blobber
from textblob.classifiers import NaiveBayesClassifier
from textblob.taggers import NLTKTagger
from textblob.wordnet import VERB

from flask_restplus import Resource, Api, fields

#Pandas for operate with Dataframes
import pandas as pd
import pandas.io.sql as sqlio
#datetime to request system time to provide information on errors
import datetime
import psycopg2
from psycopg2 import Error

# Import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global variables to be use between functions
# and system parameters
Options_list = ('Translate','Identify','Descriptor','Sentiment')
sent_level_list = ('word','sentece','whole')

# Gibberish factor, based on this the system will send an error notifying the user that the text 
# sent to analyze contain more gibberish than the allowed
Gib_factor = 0.5

#Total number of characters allowed
max_txt = 1000000
# max size in bytes allowed
max_file_size = 1000000 

# Stopwords
stopwords = stopwords.words('english')

# the dictionary will contain the description fo ISO 639-1 language code
language_desc = dict([('ab', 'Abkhaz'),
('aa', 'Afar'),
('af', 'Afrikaans'),
('ak', 'Akan'),
('sq', 'Albanian'),
('am', 'Amharic'),
('ar', 'Arabic'),
('an', 'Aragonese'),
('hy', 'Armenian'),
('as', 'Assamese'),
('av', 'Avaric'),
('ae', 'Avestan'),
('ay', 'Aymara'),
('az', 'Azerbaijani'),
('bm', 'Bambara'),
('ba', 'Bashkir'),
('eu', 'Basque'),
('be', 'Belarusian'),
('bn', 'Bengali'),
('bh', 'Bihari'),
('bi', 'Bislama'),
('bs', 'Bosnian'),
('br', 'Breton'),
('bg', 'Bulgarian'),
('my', 'Burmese'),
('ca', 'Catalan; Valencian'),
('ch', 'Chamorro'),
('ce', 'Chechen'),
('ny', 'Chichewa; Chewa; Nyanja'),
('zh', 'Chinese'),
('cv', 'Chuvash'),
('kw', 'Cornish'),
('co', 'Corsican'),
('cr', 'Cree'),
('hr', 'Croatian'),
('cs', 'Czech'),
('da', 'Danish'),
('dv', 'Divehi; Maldivian;'),
('nl', 'Dutch'),
('dz', 'Dzongkha'),
('en', 'English'),
('eo', 'Esperanto'),
('et', 'Estonian'),
('ee', 'Ewe'),
('fo', 'Faroese'),
('fj', 'Fijian'),
('fi', 'Finnish'),
('fr', 'French'),
('ff', 'Fula'),
('gl', 'Galician'),
('ka', 'Georgian'),
('de', 'German'),
('el', 'Greek, Modern'),
('gn', 'Guaraní'),
('gu', 'Gujarati'),
('ht', 'Haitian'),
('ha', 'Hausa'),
('he', 'Hebrew (modern)'),
('hz', 'Herero'),
('hi', 'Hindi'),
('ho', 'Hiri Motu'),
('hu', 'Hungarian'),
('ia', 'Interlingua'),
('id', 'Indonesian'),
('ie', 'Interlingue'),
('ga', 'Irish'),
('ig', 'Igbo'),
('ik', 'Inupiaq'),
('io', 'Ido'),
('is', 'Icelandic'),
('it', 'Italian'),
('iu', 'Inuktitut'),
('ja', 'Japanese'),
('jv', 'Javanese'),
('kl', 'Kalaallisut'),
('kn', 'Kannada'),
('kr', 'Kanuri'),
('ks', 'Kashmiri'),
('kk', 'Kazakh'),
('km', 'Khmer'),
('ki', 'Kikuyu, Gikuyu'),
('rw', 'Kinyarwanda'),
('ky', 'Kirghiz, Kyrgyz'),
('kv', 'Komi'),
('kg', 'Kongo'),
('ko', 'Korean'),
('ku', 'Kurdish'),
('kj', 'Kwanyama, Kuanyama'),
('la', 'Latin'),
('lb', 'Luxembourgish'),
('lg', 'Luganda'),
('li', 'Limburgish'),
('ln', 'Lingala'),
('lo', 'Lao'),
('lt', 'Lithuanian'),
('lu', 'Luba-Katanga'),
('lv', 'Latvian'),
('gv', 'Manx'),
('mk', 'Macedonian'),
('mg', 'Malagasy'),
('ms', 'Malay'),
('ml', 'Malayalam'),
('mt', 'Maltese'),
('mi', 'Māori'),
('mr', 'Marathi (Marāṭhī)'),
('mh', 'Marshallese'),
('mn', 'Mongolian'),
('na', 'Nauru'),
('nv', 'Navajo, Navaho'),
('nb', 'Norwegian Bokmål'),
('nd', 'North Ndebele'),
('ne', 'Nepali'),
('ng', 'Ndonga'),
('nn', 'Norwegian Nynorsk'),
('no', 'Norwegian'),
('ii', 'Nuosu'),
('nr', 'South Ndebele'),
('oc', 'Occitan'),
('oj', 'Ojibwe, Ojibwa'),
('cu', 'Old Church Slavonic'),
('om', 'Oromo'),
('or', 'Oriya'),
('os', 'Ossetian, Ossetic'),
('pa', 'Panjabi, Punjabi'),
('pi', 'Pāli'),
('fa', 'Persian'),
('pl', 'Polish'),
('ps', 'Pashto, Pushto'),
('pt', 'Portuguese'),
('qu', 'Quechua'),
('rm', 'Romansh'),
('rn', 'Kirundi'),
('ro', 'Romanian, Moldavan'),
('ru', 'Russian'),
('sa', 'Sanskrit (Saṁskṛta)'),
('sc', 'Sardinian'),
('sd', 'Sindhi'),
('se', 'Northern Sami'),
('sm', 'Samoan'),
('sg', 'Sango'),
('sr', 'Serbian'),
('gd', 'Scottish Gaelic'),
('sn', 'Shona'),
('si', 'Sinhala, Sinhalese'),
('sk', 'Slovak'),
('sl', 'Slovene'),
('so', 'Somali'),
('st', 'Southern Sotho'),
('es', 'Spanish; Castilian'),
('su', 'Sundanese'),
('sw', 'Swahili'),
('ss', 'Swati'),
('sv', 'Swedish'),
('ta', 'Tamil'),
('te', 'Telugu'),
('tg', 'Tajik'),
('th', 'Thai'),
('ti', 'Tigrinya'),
('bo', 'Tibetan'),
('tk', 'Turkmen'),
('tl', 'Tagalog'),
('tn', 'Tswana'),
('to', 'Tonga'),
('tr', 'Turkish'),
('ts', 'Tsonga'),
('tt', 'Tatar'),
('tw', 'Twi'),
('ty', 'Tahitian'),
('ug', 'Uighur, Uyghur'),
('uk', 'Ukrainian'),
('ur', 'Urdu'),
('uz', 'Uzbek'),
('ve', 'Venda'),
('vi', 'Vietnamese'),
('vo', 'Volapük'),
('wa', 'Walloon'),
('cy', 'Welsh'),
('wo', 'Wolof'),
('fy', 'Western Frisian'),
('xh', 'Xhosa'),
('yi', 'Yiddish'),
('yo', 'Yoruba'),
('za', 'Zhuang, Chuang'),
('zu', 'Zulu')])


###
### CROSS FUNCTIONS to be used for all the options
###

def crearConexion():
    
    connection = psycopg2.connect(user = "m.soto.montesinos",
                                      password = "XXXXXX",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "twitterBBVA")

    return connection

def obtenerTweets():

    try:
        
        connection = crearConexion()

        query = "select status_id, text from training_set"
        
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
    
# First function, to get the files from the web
def getfile(Input:"String list or url with the file"):

    # we validate that the URL is being populated
    if Input == "":
        return ("NO OK", "URL not informed", "")
    
    # retrieve header to validate the size of the file
    try:
        response = requests.head(Input)
    except requests.exceptions.MissingSchema:
        return ("NO OK","Invalid URL","")
    except requests.exceptions.Timeout:
        return ("NO OK","Time Out reaching for the file - please try again in a few minutes","")
    except requests.exceptions as get_error:
        return ("NO OK", get_error,"")

    # if the size of the file is over the max allowed, we stop
    if int(response.headers['content-length']) > max_file_size:
        return  ("NO OK","File too big")
    try:
        file_get  = requests.get(Input,stream = True)
        
    # using get, we retrieve the file from the URL
    except requests.exceptions.MissingSchema:
        return ("NO OK","Invalid URL","")
    except requests.exceptions.Timeout:
        return ("NO OK","Time Out reaching for the file - please try again in a few minutes","")
    except requests.exceptions as get_error:
        return ("NO OK", get_error,"")

    text = file_get.text
    return("OK", "",text)


# General Input validations
def validations(txt_input:"Text to be validated",Option:"Option to be applied",sent_level=""):
    global Gib_factor
    global max_txt
    global Options_list
    global sent_level_list
    
    decorators = [limiter.limit("60/minute")]
    
    if Option not in Options_list:
        return("NO OK","Option not valid")
    if Option == "Sentiment" and sent_level not in sent_level_list:
        return("NO OK","Option not valid")
    if len(txt_input) > max_txt:
        return("NO OK","Text too big. The total number of admitted characters is "+str(max_txt))
    if txt_input =="" :
        return("NO OK","Input empty")
    else:
        # using Textblob, we identify the language
        tb_text = TextBlob(txt_input)
        lng_txt = tb_text.detect_language()
        if lng_txt == 'en':
            if Option == "Translate":
                return ("NO OK", "Input should be a text and in a lengauage different than English")
            err_word = 0
            for word, pos in tb_text.tags:
                # to validate if the word is valid, we cross it with the dictionary
                ret_word = word.synsets
                if ret_word ==[]:
                    err_word = err_word +1
            # we validate the amount of possible Gibberish words agains the system factor
            if len(tb_text.tags) == 0:
                return ("NO OK","Input doesn't contain actual text")
            elif err_word/len(tb_text.tags)>Gib_factor:
                return ("NO OK","Possible Gibberish")
        elif lng_txt == 'fy':
            return ("NO OK", "Language not supperted/not possible to identify")
        elif lng_txt != "en" and Option != "Translate" and Option != "Identify":
            return ("NO OK","For other than English the only options available are Translate/Identify language")

    return("OK","")


# Error function to print the possible information that it would help to fix errors    
def print_error(Option,input_txt,type_input,page,error):
    currentDT = datetime.datetime.now()
    print("********************************************************ERROR********************************************************")
    print("********************************************************ERROR********************************************************")
    print("**  Error found while processing file, at:",currentDT)
    print("**  The error found was:",error)
    print("**  The first 10 characters of the text is",input_txt[1:10])
    print("**  The option used:",Option)
    print("**  The URL provided:",page)
    print("********************************************************ERROR********************************************************")
    print("********************************************************ERROR********************************************************")
    return(None)


###
### FEATURES to provide capabilities on the APIs
###


# Check Spelling
def spell_check(txt_input:"text to spellcheck"):
    tb_text = TextBlob(txt_input)
    tb_update = tb_text.correct()
    return("OK","",tb_update)
  
# Function to identify descriptors and quantify their appearance on the input file
def Descriptors(File_name:"Name of the file with the characters"):
    tb_text = TextBlob(File_name)
    adj_list =[]
    # Once the TextBlob is created, a loop is performed over the list of words
    # to identify the descriptors (PoS like JJ are adjectives)
    for word,pos in tb_text.tags:
        if pos[0:2] =="JJ":
            adj_list.append(word)
    # Creating a Dataframe indicating how many times the adjective is on the list
    adj_list_df = pd.DataFrame({'Descriptor':adj_list})
    count_desc = adj_list_df['Descriptor'].value_counts(sort=False).sort_values(ascending=False)
    count_df = count_desc.rename_axis('Descriptor').reset_index(name='Occurences')
    return("OK","",count_df)


# Identify Language function
def identify_language(txt_input:"text to identify language"):

    global language_desc

    tb_text = TextBlob(txt_input)
    lng_txt = tb_text.detect_language()

    if lng_txt in language_desc:
        lng_desc = language_desc[lng_txt]
    else:
        lng_desc = lng_txt

    return("OK","","The language of the input is "+lng_desc)

# Translate Language function
def Translate_to_english(txt_input:"text to translate language"):
    tb_text = TextBlob(txt_input)
    lng_txt = tb_text.detect_language()
    txt_output = tb_text.translate(from_lang=lng_txt,to="en")
    
    return("OK","",txt_output)


# Sentiment
def identify_sentiment(txt_input:"text to identify language",sent_level:"level to perform the sentiment"):

    count_pos = 0
    count_neg = 0
    total_pos = 0
    total_neg = 0
    overall = 0
    tb_text = TextBlob(txt_input)
    if sent_level =="word":
        for word in tb_text.words:
            word_tb = TextBlob(str(word))
            sentiment_value = word_tb.sentiment.polarity
            if sentiment_value >0:
                count_pos = count_pos + 1
                total_pos = total_pos + sentiment_value
            elif sentiment_value < 0:
                count_neg = count_neg + 1
                total_neg = total_neg + sentiment_value
    elif sent_level == "sentence":
        for sentence in tb_text.sentences:
            sentence_tb = TextBlob(str(sentence))
            sentiment_value = sentence_tb.sentiment.polarity
            if sentiment_value >0:
                count_pos = count_pos + 1
                total_pos = total_pos + sentiment_value
            elif sentiment_value < 0:
                count_neg = count_neg + 1
                total_neg = total_neg + sentiment_value
    else:
        sentiment_value = tb_text.sentiment.polarity
        if sentiment_value >=0:
            count_pos = count_pos + 1
            total_pos = total_pos + sentiment_value
        else:
            count_neg = count_neg + 1
            total_neg = total_neg + sentiment_value 
    overall = total_pos + total_neg
    if count_pos + count_neg > 0:
        overall_ave = (total_pos + total_neg) / (count_pos+count_neg)
    else:
        overall_ave = 0
    if count_pos > 0:
        ave_pos = total_pos / count_pos
    else:
        ave_pos = 0
        
    if count_neg > 0:
        ave_neg = total_neg / count_neg
    else:
        ave_neg = 0
    sentiment_d = {'Value':["Overall","Possitive","Negative"],"Sentiment Average":[overall_ave,ave_pos,ave_neg],"Total Elements":[count_neg+count_pos,count_pos,count_neg]}
    print(sentiment_d)
    df_sentiment = pd.DataFrame(data=sentiment_d)
    return("OK","",df_sentiment)

# Main Topic
def main_topic(txt_input:"text to identify main topic"): 
    # Convert to Blob
    tb_text = TextBlob(txt_input)
    
    # Lemmatize
    out = " ". join([w.lemmatize() for w in tb_text.words])
    
    # Tokenize into words
    word_tokens = TextBlob(out).words    
    
    # Remove stop words
    lista = [word for word in word_tokens if word not in stopwords]
    tekst = ' '.join(lista)
    blob = TextBlob(tekst)
    
    # N-Grams

    if len(lista)<3:
        return("OK","","The main topic is "+ str(blob))
    else:
        blob_n = blob.ngrams(3)
        n_list = []
        for l in blob_n:
            n_list.append(str(l))
            n_count = pd.DataFrame({'NGram':n_list})    
            count_n = n_count['NGram'].value_counts(sort=False).sort_values(ascending=False)
            return("OK","","The main topic is "+ str(count_n.index[0]))



# definition of the REST API
app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5000 per hour"]
)
##################################################################################
##################################################################################
##################      END POINTS      ##########################################
##################      END POINTS      ##########################################
##################      END POINTS      ##########################################
##################################################################################
##################################################################################


##################################################################################
#### Main End Point in the case that the user prefer to target only one
##################################################################################
@app.route('/midterm/main', methods=['GET'])

def main_process():
    decorators = [limiter.limit("60/minute")]
    results = [
        {
          "End Point": "/midterm/SpellCheck",
          "Description": "Correct spelling mistakes in the input text.",
          "Parameters" :  {"1. type" : "method used for submitting the file: 'url' or 'str' - Mandatory",
                           "2. url" : "URL from where to get the file - Optional",
                           "3.text" : "Text to be proce'ssed if URL is not submited - Optional"
                           }
          
        },
        {
          "End Point": "/midterm/Descriptor",
          "Description": "Identify all the different descriptors and quantify the number of times they appear. The List will be sorted Descending. Available only in English",
          "Parameters" :  {"1. type" : "method used for submitting the file: 'url' or 'str' - Mandatory",
                           "2. url" : "URL from where to get the file - Optional",
                           "3.text" : "Text to be proce'ssed if URL is not submited - Optional"
                           }
          
        },
        {
          "End Point": "/midterm/Identify",
          "Description": "review the text to identify the language. Available on the 161 languages",
          "Parameters" :  {"1. type" : "method used for submitting the file: 'url' or 'str' - Mandatory",
                           "2. url" : "URL from where to get the file - Optional",
                           "3.text" : "Text to be proce'ssed if URL is not submited - Optional"
                           }
          },
        {
          "End Point": "/midterm/Translate",
          "Description": "Return an English version of the text submitted.",
          "Parameters" :  {"1. type" : "method used for submitting the file: 'url' or 'str' - Mandatory",
                           "2. url" : "URL from where to get the file - Optional",
                           "3.text" : "Text to be proce'ssed if URL is not submited - Optional"
                           }
          },
        {
          "End Point": "/midterm/Sentiment",
          "Description": "Polarize the text submitted (whole text, sentences or words – based on the request-) with a value between -1 (negative) to 1 (positive). Available only in English.",
          "Parameters" : {"word" : "word",
                           "sentence" : "Sentence",
                           "whole" : "the whole text"}
    },
        {
          "End Point": "/midterm/MainTopic",
          "Description": "Identify the main topic of the text submitted by finding the most common sets of words.  Available only in English for stopword removal but can be used for all languages.",
          "Parameters" : {"1. type" : "method used for submitting the file: 'url' or 'str' - Mandatory",
                           "2. url" : "URL from where to get the file - Optional",
                           "3.text" : "Text to be processed if URL is not submited - Optional"
                           }
    }
    ]
    return make_response(jsonify(results),200)


##################################################################################
#### Spellcheck End Point
##################################################################################
    
@app.route('/midterm/SpellCheck', methods=['GET'])

def spellcheck_process():
    
 
    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)
    Option = "SpellCheck"

    if type_input == 'url':
        result,error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option,input_txt,type_input,page,error)
            return make_response(jsonify({"error":error}), 400)
        
    result,error = validations(input_txt,Option)

    if result != "OK":
        print_error(Option,input_txt,type_input,page,error)
        return make_response(jsonify({"error":error}), 400)

    result,error,spellcheck_result = spell_check(input_txt)

    result_return = spellcheck_result.to_json(orient='split')

    if result =="OK":
        return make_response(result_return, 200)
    else:
        return make_response(jsonify({"error":error}), 400)


##################################################################################
#### Descriptors End Point
##################################################################################
    
@app.route('/midterm/Descriptor', methods=['GET'])

def Descriptors_process():
    
 
    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)
    Option = "Descriptor"

    if type_input == 'url':
        result,error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option,input_txt,type_input,page,error)
            return make_response(jsonify({"error":error}), 400)
        
    result,error = validations(input_txt,Option)

    if result != "OK":
        print_error(Option,input_txt,type_input,page,error)
        return make_response(jsonify({"error":error}), 400)

    result,error,desciption_result = Descriptors(input_txt)

    result_return = desciption_result.to_json(orient='split')

    if result =="OK":
        return make_response(result_return, 200)
    else:
        return make_response(jsonify({"error":error}), 400)


##################################################################################
#### Identify End Point
##################################################################################
    
@app.route('/midterm/Identify', methods=['GET'])

def Identify_process():

    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)

    Option = "Identify"

    if type_input == 'url':
        result, error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option, input_txt, type_input, page, error)
            return make_response(jsonify({"error": error}), 400)

    result, error = validations(input_txt, Option)

    if result != "OK":
        print_error(Option, input_txt, type_input, page, error)
        return make_response(jsonify({"error": error}), 400)

    result,error,result_return = identify_language(input_txt)
    
    if result =="OK":
        return make_response(jsonify({"Result":result_return}), 200)
    else:
        return make_response(jsonify({"error":error}), 400)



##################################################################################
#### Translate End Point
##################################################################################
    
@app.route('/midterm/Translate', methods=['GET'])

def Translate_process():
    
   
    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)

    Option = "Translate"

    if type_input == 'url':
        result, error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option, input_txt, type_input, page, error)
            return make_response(jsonify({"error": error}), 400)

    result, error = validations(input_txt, Option)

    if result != "OK":
        print_error(Option, input_txt, type_input, page, error)
        return make_response(jsonify({"error": error}), 400)

    result,error,result_return = Translate_to_english(input_txt)
    
    if result == "OK":
        return make_response(jsonify({"Original Text": input_txt},{"Translation Text": str(result_return)},), 200)
    else:
        return make_response(jsonify({"error": error}), 400)

##################################################################################
#### Sentiment End Point
##################################################################################
    
@app.route('/midterm/Sentiment', methods=['GET'])

def Sentiment_process():

  
    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)
    sent_level = request.args.get('level', default="", type=str)

    Option = "Sentiment"

    if type_input == 'url':
        result, error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option, input_txt, type_input, page, error)
            return make_response(jsonify({"error": error}), 400)

    result, error = validations(input_txt, Option,sent_level)

    if result != "OK":
        print_error(Option, input_txt, type_input, page, error)
        return make_response(jsonify({"error": error}), 400)

    result, error, sentiment_result = identify_sentiment(input_txt,sent_level)
    result_return = sentiment_result.to_json(orient='split')

    if result == "OK":
        return make_response(result_return, 200)
    else:
        return make_response(jsonify({"error": error}), 400)

##################################################################################
#### Main Topic End Point
##################################################################################
    
@app.route('/midterm/MainTopic', methods=['GET'])

def Main_process():
    
 
    page = request.args.get('url', default= "",type=str)
    type_input = request.args.get('type', default ="" , type=str)
    input_txt = request.args.get('text', default ="" , type=str)
    Option = "MainToipc"

    if type_input == 'url':
        result,error, input_txt = getfile(page)
        if result != "OK":
            print_error(Option,input_txt,type_input,page,error)
            return make_response(jsonify({"error":error}), 400)
        
    result,error = validations(input_txt,Option)

    if result != "OK":
        print_error(Option,input_txt,type_input,page,error)
        return make_response(jsonify({"error":error}), 400)

    result,error,main_topic_result = main_topic(input_txt)

    result_return = main_topic_result.to_json(orient='split')

    if result =="OK":
        return make_response(result_return, 200)
    else:
        return make_response(jsonify({"error":error}), 400)


##
#  GET request for the user instructions and POST requests to submit data,
##

api = Api(app = app ,
		  version = "1.0",
		  title = "NLP Processor",
		  description = "NLP Data Service provides severa Natural Languauge Processing services")
###


model = api.model('Name Model',
				  {'input': fields.String(required = True,
    					  				 description="Name of the person",
    					  				 help="Name cannot be blank.")})

####
## Parts of speech End points for get and post
####
pos_space = api.namespace('PartsOfSpeech', description='Pass a string to recognize the parts of speech')

@pos_space.route("/pos")
class PartsOfSpeech(Resource):
    decorators = [limiter.limit("60/minute")]
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={})
    def get(self):
        try:
            return {
                "instructions": "The sample call to the POST method will take in as input a JSON with an element called input",
            }
        except KeyError as e:
            pos_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            pos_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={ 'input': 'Specify the input string that needs to be processed' })
    @api.expect(model)
    def post(self):
            try:
                inputData=request.json['input']
                wiki = TextBlob(inputData)
                return {
                    "pos" : wiki.tags
                }

            except KeyError as e:
                pos_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
            except Exception as e:
                pos_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")



####
## Subjectivity End points for get and post
####
sub_space = api.namespace('Subjectivity', description='Pass a string to reconnize the subjectivity or objectivity of the text')

@sub_space.route("/sub")
class Subjectivity(Resource):
    decorators = [limiter.limit("60/minute")]
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={})
    def get(self):
        try:
            return {
                "instructions": "The sample call to the POST method will take in as input a JSON with an element called input",
            }
        except KeyError as e:
            sub_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            sub_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={ 'input': 'Specify the input string that needs to be processed' })
    @api.expect(model)
    def post(self):
            try:
                inputData=request.json['input']
                wiki = TextBlob(inputData)
                return {
                    "subjectivityScore": wiki.subjectivity,
                }

            except KeyError as e:
                sub_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
            except Exception as e:
                sub_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")



####
## Lemmatization  End points for get and post
####
lem_space = api.namespace('Lemmatize', description='Pass a string and its words will be lemmatized')

@lem_space.route("/lemmatize")
class Lemmatize(Resource):
    decorators = [limiter.limit("60/minute")]
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={})
    def get(self):
        try:
            return {
                "instructions": "The sample call to the POST method will take in as input a JSON with an element called input",
            }
        except KeyError as e:
            lem_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            lem_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' },
             params={ 'input': 'Specify the input string that needs to be processed' })
    @api.expect(model)
    def post(self):
            try:
                inputData=request.json['input']
                wiki = TextBlob(inputData)
                print(wiki.words)
                lemmatized_sentence = "LEMMATIZED ="
                for word  in wiki.words:
                    lemmatized_sentence =  lemmatized_sentence+" "+str(word.lemmatize())
                    print(lemmatized_sentence )
                return {
                    "lemmatized_word" : lemmatized_sentence
                }

            except KeyError as e:
                lem_space.abort(500, e.__doc__, status = "Could not save information", statusCode = "500")
            except Exception as e:
                lem_space.abort(400, e.__doc__, status = "Could not save information", statusCode = "400")

  
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    tweets = obtenerTweets()

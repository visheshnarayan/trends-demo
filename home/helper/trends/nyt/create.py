# imports
import pandas as pd
import nltk, os, json
from gensim.models import Word2Vec

from home.helper.process import rem_stop_words

BASE_DIR = "./home/helper/trends/nyt/"

# labels
labels = ["jan20", "aug20", "dec20", "jan21", "aug21", "dec21"]

def create_nyt():
    print(os.getcwd())
    jan20 = pd.read_csv(BASE_DIR + "data/jan1.csv", delimiter = "/t", engine='python')
    aug20 = pd.read_csv(BASE_DIR + "data/aug1.csv", delimiter = "/t", engine='python')
    dec20 = pd.read_csv(BASE_DIR + "data/dec1.csv", delimiter = "/t", engine='python')
    jan21 = pd.read_csv(BASE_DIR + "data/jan2.csv", delimiter = "/t", engine='python')
    aug21 = pd.read_csv(BASE_DIR + "data/aug2.csv", delimiter = "/t", engine='python')
    dec21 = pd.read_csv(BASE_DIR + "data/dec2.csv", delimiter = "/t", engine='python')

    # select data
    jan20 = jan20['Headlines'].map(str) + '. ' + jan20['Glances'].map(str)
    aug20 = aug20['Headlines'].map(str) + '. ' + aug20['Glances'].map(str)
    dec20 = dec20['Headlines'].map(str) + '. ' + dec20['Glances'].map(str)
    jan21 = jan21['Headlines'].map(str) + '. ' + jan21['Glances'].map(str)
    aug21 = aug21['Headlines'].map(str) + '. ' + aug21['Glances'].map(str)
    dec21 = dec21['Headlines'].map(str) + '. ' + dec21['Glances'].map(str)

    # list for clean data
    cleaned_jan20 = []
    cleaned_aug20 = []
    cleaned_dec20 = []
    cleaned_jan21 = []
    cleaned_aug21 = []
    cleaned_dec21 = []

    # clean data
    for k in jan20: cleaned_jan20.append(''.join(rem_stop_words(k)))
    for k in aug20: cleaned_aug20.append(''.join(rem_stop_words(k)))
    for k in dec20: cleaned_dec20.append(''.join(rem_stop_words(k)))

    for k in jan21: cleaned_jan21.append(''.join(rem_stop_words(k)))
    for k in aug21: cleaned_aug21.append(''.join(rem_stop_words(k)))
    for k in dec21: cleaned_dec21.append(''.join(rem_stop_words(k)))

    # Tokenize
    jan20_vectors = [nltk.word_tokenize(x) for x in cleaned_jan20]
    aug20_vectors = [nltk.word_tokenize(x) for x in cleaned_aug20]
    dec20_vectors = [nltk.word_tokenize(x) for x in cleaned_dec20]

    jan21_vectors = [nltk.word_tokenize(x) for x in cleaned_jan21]
    aug21_vectors = [nltk.word_tokenize(x) for x in cleaned_aug21]
    dec21_vectors = [nltk.word_tokenize(x) for x in cleaned_dec21]

    # create and save models
    j0 = Word2Vec(jan20_vectors)
    a0 = Word2Vec(aug20_vectors)
    d0 = Word2Vec(dec20_vectors)

    j1 = Word2Vec(jan21_vectors)
    a1 = Word2Vec(aug21_vectors)
    d1 = Word2Vec(dec21_vectors)

    # saving models
    j0.save(BASE_DIR + "models/jan20.model")
    a0.save(BASE_DIR + "models/aug20.model")
    d0.save(BASE_DIR + "models/dec20.model")

    j1.save(BASE_DIR + "models/jan21.model")
    a1.save(BASE_DIR + "models/aug21.model")
    d1.save(BASE_DIR + "models/dec21.model")

    data = {}

    data["jan20"] = j0.wv.index_to_key
    data["aug20"] = a0.wv.index_to_key
    data["dec20"] = d0.wv.index_to_key
    data["jan21"] = j1.wv.index_to_key
    data["aug21"] = a1.wv.index_to_key
    data["dec21"] = d1.wv.index_to_key


    data["common"] = list(set(data["jan20"]) & set(data["aug20"]) & set(data["dec20"]) & set(data["jan21"]) & set(data["aug21"]) & set(data["dec21"]))

    with open(BASE_DIR + 'words.json', 'w') as fp:
        json.dump(data, fp, indent=4)


    
    



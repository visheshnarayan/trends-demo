# imports
import pandas as pd
import nltk, os
from gensim.models import Word2Vec
from scipy.spatial import distance

from .process import convert, rem_stop_words

def nyt_trends(base_term, rel_terms):
    # load dataset
    print(os.getcwd())
    jan20 = pd.read_csv("./home/helper/data/nyt/jan1.csv", delimiter = "/t", engine='python')
    aug20 = pd.read_csv("./home/helper/data/nyt/aug1.csv", delimiter = "/t", engine='python')
    dec20 = pd.read_csv("./home/helper/data/nyt/dec1.csv", delimiter = "/t", engine='python')
    jan21 = pd.read_csv("./home/helper/data/nyt/jan2.csv", delimiter = "/t", engine='python')
    aug21 = pd.read_csv("./home/helper/data/nyt/aug2.csv", delimiter = "/t", engine='python')
    dec21 = pd.read_csv("./home/helper/data/nyt/dec2.csv", delimiter = "/t", engine='python')

    # select data
    jan20 = jan20['Headlines'].map(str) + '. ' + jan20['Glances'].map(str)
    aug20 = aug20['Headlines'].map(str) + '. ' + aug20['Glances'].map(str)
    dec20 = dec20['Headlines'].map(str) + '. ' + dec20['Glances'].map(str)
    jan21 = jan21['Headlines'].map(str) + '. ' + jan21['Glances'].map(str)
    aug21 = aug21['Headlines'].map(str) + '. ' + aug21['Glances'].map(str)
    dec21 = dec21['Headlines'].map(str) + '. ' + dec21['Glances'].map(str)

    # labels
    labels = ["jan20", "aug20", "dec20", "jan21", "aug21", "dec21"]

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

    # Create W2V models
    models = []

    models.append(Word2Vec(jan20_vectors))
    models.append(Word2Vec(aug20_vectors))
    models.append(Word2Vec(dec20_vectors))

    models.append(Word2Vec(jan21_vectors))
    models.append(Word2Vec(aug21_vectors))
    models.append(Word2Vec(dec21_vectors))

    # get similarity scores
    values = []

    # looping through all relative terms
    for idx, rel in enumerate(rel_terms):
        # looping through all models
        vals = []
        for i, model in enumerate(models):
            # TODO : Add logic for if base term does not exist
            # TODO : add logic to handle if term not present

            try:
                vals.append(distance.cosine(model.wv[base_term], model.wv[rel]))
            except Exception as e:
                if not vals:
                    vals.append(1.0)
                else:
                    vals.append(vals[-1])

                print(f"Exception occured in model: {model}, number: {i}\nbase term: {base_term}, relative term: {rel}")
        values.append(vals)

    # creating dataready
    dataready = convert(rel_terms, values)

    # returning values
    return labels, dataready


    
    



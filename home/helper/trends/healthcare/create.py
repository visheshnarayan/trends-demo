# imports
import pandas as pd
import nltk, os, json
from gensim.models import Word2Vec

from home.helper.process import rem_stop_words
from home.helper.transform import common_terms

BASE_DIR = "./home/helper/trends/healthcare/"

# labels (discarding : ["2013", "2014", "2015"] )
labels = ["2016", "2017", "2018", "2019"]

def add_year():
    df = pd.read_csv(BASE_DIR + "data/health_data_full.csv")
    make_year = lambda row: str(row["inspection_date"][-4:])

    df["year"] = df.apply(make_year, axis=1)

    # saving the dataframe
    df.to_csv(BASE_DIR + "data/health_data_full.csv", index=False)

def create_healthcare():
    print(os.getcwd())
    print(len(labels), labels)

    # read all data
    dfs = []
    for label in labels:
        df_loc = BASE_DIR + f"data/{label}.csv"
        dfs.append(pd.read_csv(df_loc))

    # print(len(dfs), dfs)

    # getting all the text data
    datasets = []
    for df in dfs:
        datasets.append(df["inspection_text"].map(str))

    # clean data
    cleaned_datasets = []
    for idx, data in enumerate(datasets):
        print(f"..{idx+1}")
        temp = []

        for k in data: 
            # print("==", end="")
            temp.append(rem_stop_words(k))
        cleaned_datasets.append(temp)

    # print(len(cleaned_datasets), cleaned_datasets)

    # tokenizing data
    vectors = []
    for data in cleaned_datasets:
        temp = [nltk.word_tokenize(x) for x in data]
        vectors.append(temp)

    # print(len(vectors), vectors)

    # create models
    models = []
    for vector in vectors:
        models.append(Word2Vec(vector))

    print(len(models), models)

    # save model
    for idx, model in enumerate(models):
        model.save(BASE_DIR + f"models/{labels[idx]}.model")

def create_common_words():
    # loading models
    models = []
    for label in labels:
        models.append(Word2Vec.load(BASE_DIR + f"models/{label}.model"))

    # creating list of lists of all terms in each model
    terms = []
    for model in models:
        terms.append(model.wv.index_to_key)

    # creating dict to save to json gor common words for all labels
    words_data = {}

    print(len(terms), terms)

    for idx, label in enumerate(labels):
        words_data[label] = terms[idx]

    words_data["common"] = common_terms(terms)

    # saving words data
    with open(BASE_DIR + 'words.json', 'w') as fp:
        json.dump(words_data, fp, indent=4)

# imports
import pandas as pd

def reverse_healthcare(base, r1, r2, sub_model):
    '''
    reverse_nyt: Reverse queries for documents with base, r1, and r2 for New York Times August 2020 dataset
    return: a dictionary containing key:value pairs in the form of docID:[base_loc, r1_loc, r2_loc]
    
    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path=f"home/helper/trends/healthcare/data/{sub_model}.csv"

    # load in data
    # U+000A -> unicode for line break
    text=pd.read_csv(path, sep="U+000A", engine="python")
    text.columns=['text']

    #lower case for querying
    text['text']=text['text'].str.lower()

    # assign ID value to each row
    text['id']=text.index
    
    # locs dictionary
    locs={}

    # filtered dataframe containing only texts with all base, r1, and r2
    text=text[text['text'].str.contains(base) & text['text'].str.contains(r1) & text['text'].str.contains(r2)]

    # iteration over all texts to save location of words
    for index, row in text.iterrows():
        locs[text['id'][index]]=[
            text['text'][index].index(base),
            text['text'][index].index(r1),
            text['text'][index].index(r2)
        ]
    return locs
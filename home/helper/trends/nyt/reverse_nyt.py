# imports
import pandas as pd

def reverse_nyt(base, r1, r2, sub_model):
    '''
    reverse_nyt: Reverse queries for documents with base, r1, and r2 for New York Times August 2020 dataset
    return: a dictionary containing key:value pairs in the form of docID:[base_loc, r1_loc, r2_loc]
    
    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path="home/helper/trends/nyt/data/"+get_path(sub_model)+".csv"

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

def get_path(sub_model):
    '''
    get_path: Helper function for retrieving file associated with sub_model given
    return: string, file name of csv file

    Parameters:
    sub_mode: string (name of model)
    '''
    if sub_model=="aug20":
        return "aug1"
    if sub_model=="aug21":
        return "aug2"
    if sub_model=="dec20":
        return "dec1"
    if sub_model=="dec21":
        return "dec2"
    if sub_model=="jan20":
        return "jan1"
    if sub_model=="jan21":
        return "jan2"
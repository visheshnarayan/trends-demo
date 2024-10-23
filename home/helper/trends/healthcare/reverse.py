# imports
import pandas as pd
import re

def reverse_healthcare(base, r1, r2):
    '''
    reverse_healthcare: Reverse queries for documents with base, r1, and r2 for all text data in Healthcare
    return: a list containing all docs with base, r1, and r2
    
    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path = "home/helper/trends/healthcare/data/full.csv"

    # load in data
    # text=pd.read_csv(path)
    text=pd.read_csv(path)

    # clean 
    def clean(df):
        '''
        cleaning procedure for healthcare text data 
        '''
        # added .copy() to avoid SettingWithCopyWarning
        # https://www.analyticsvidhya.com/blog/2021/11/3-ways-to-deal-with-settingwithcopywarning-in-pandas/
        df=df[["inspection_text"]].copy()

        # replace texts
        df["inspection_text"]=df["inspection_text"].apply(lambda text: text.replace("**NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY** ", ""))
        df["inspection_text"]=df["inspection_text"].apply(lambda text: text.replace("<BR/>", ""))
        df["inspection_text"]=df["inspection_text"].apply(lambda text: text.replace(">", ""))
        return df

    # cleaned df
    text=clean(text)

    # lower and remove punctuation
    text["clean"]=text["inspection_text"].apply(lambda text: text.lower())
    text["clean"]=text["clean"].apply(lambda text: re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text))

    # tokenize
    text["tokens"]=text["clean"].apply(lambda text: text.split())

    # query for base -> keep if text has r1 or r2
    def filter(tokens):
        if base.lower() in tokens:
            if r1.lower() in tokens or r2.lower() in tokens:
                return 1
        return 0
    text["valid"]=text["tokens"].apply(lambda tokens: filter(tokens))


    # list of strings containing base with r1 or r2 that passed filter function with return of 1
    # drop(axis=1, labels=["tokens"]) because drop_duplicates() does not work with hashables in dataframe column
    text=text.query("valid==1").drop(axis=1, labels=["tokens"]).drop_duplicates()["Headlines"].to_list()

    # replacing apostrophe
    single = lambda x: x.replace("\'", "")

    # return finalized list of strings
    return list(map(single, text))
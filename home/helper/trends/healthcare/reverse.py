# imports
import pandas as pd

def reverse_healthcare(base, r1, r2):
    '''
    reverse_nyt: Reverse queries for documents with base, r1, and r2 for all text data in either NYT data or Healthcare data
    return: a list containing all docs with base, r1, and r2
    
    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path = "home/helper/trends/healthcare/data/full.csv"

    # load in data
    text=pd.read_csv(path)

    # (?i) -> regex ignore capitalization
    # check for base 
    text=text[text["inspection_text"].str.contains(f"(?i){base}")]

    # return list with texts containing r1 OR r2 with dropped duplicates
    text = text[text["inspection_text"].str.contains(f"(?i){r1}|{r2}")].drop_duplicates()["inspection_text"].to_list()

    # replacing apostrophe
    single = lambda x: x.replace("\'", "")
    return list(map(single, text))
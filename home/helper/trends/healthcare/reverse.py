# imports
import pandas as pd

def reverse_nyt(base, r1, r2, sub_model):
    '''
    reverse_nyt: Reverse queries for documents with base, r1, and r2 for all text data in either NYT data or Healthcare data
    return: a list containing all docs with base, r1, and r2
    
    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    sub_model: string (nyt or healthcare)
    '''
    path = "home/helper/trends/healthcare/data/full.csv"

    # load in data
    # U+000A -> unicode for line break
    text=pd.read_csv(path, sep="U+000A", engine="python")

    # (?i) -> regex ignore capitalization
    # check for base 
    text=text[text["Headlines"].str.contains(f"(?i){base}")]

    # return list with texts containing r1 OR r2 with dropped duplicates
    return text[text["Headlines"].str.contains(f"(?i){r1}|{r2}")].drop_duplicates()["Headlines"].to_list()
# # imports
# import pandas as pd
# import re

# def reverse_nyt(base, r1, r2):
#     '''
#     reverse_nyt: Reverse queries for documents with base, r1, and r2 for all text data in NYT
#     return: a list containing all docs with base, r1, and r2
    
#     Parameters:
#     base: string (word)
#     r1: string (word)
#     r2: string (word)
#     '''
#     path = "home/helper/trends/nyt/data/full.csv"

#     # load in data
#     # text=pd.read_csv(path)
#     text=pd.read_csv(path)

#     # clean
#     text["clean"]=text["text"].apply(lambda text: text.lower())
#     text["clean"]=text["clean"].apply(lambda text: re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text))

#     # tokenize
#     text["tokens"]=text["clean"].apply(lambda text: text.split())

#     # query for base -> keep if text has r1 or r2
#     def filter(tokens):
#         if base.lower() in tokens:
#             if r1.lower() in tokens or r2.lower() in tokens:
#                 return 1
#         return 0
    
#     text["valid"]=text["tokens"].apply(lambda tokens: filter(tokens))

#     # list of strings containing base with r1 or r2 that passed filter function with return of 1
#     # drop(axis=1, labels=["tokens"]) because drop_duplicates() does not work with hashables in dataframe column
#     text=text.query("valid==1").drop(axis=1, labels=["tokens"]).drop_duplicates()["text"].to_list()

#     # replacing apostrophe
#     single = lambda x: x.replace("\'", "")

#     # return finalized list of strings
#     return list(map(single, text))

# imports
import pandas as pd
import re

def reverse_nyt(base, r1, r2):
    '''
    Reverse queries for documents containing the base word and either r1 or r2 from NYT data.
    Returns a list of unique documents matching the criteria.

    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path = "home/helper/trends/nyt/data/full.csv"

    # Load data
    df = pd.read_csv(path)

    # Ensure 'text' column exists
    if 'text' not in df.columns:
        raise ValueError("Input CSV must contain 'text' column.")

    # Lowercase and clean the text
    df["clean"] = df["text"].str.lower()
    regex_pattern = r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"
    df["clean"] = df["clean"].str.replace(regex_pattern, "", regex=True)

    # Prepare regex patterns with word boundaries
    base_pattern = r"\b" + re.escape(base.lower()) + r"\b"
    r1_pattern = r"\b" + re.escape(r1.lower()) + r"\b"
    r2_pattern = r"\b" + re.escape(r2.lower()) + r"\b"

    # Check for the presence of base, r1, and r2
    df["has_base"] = df["clean"].str.contains(base_pattern, regex=True)
    df["has_r1_or_r2"] = df["clean"].str.contains(r1_pattern, regex=True) | df["clean"].str.contains(r2_pattern, regex=True)

    # Filter rows where base and (r1 or r2) are present
    df_valid = df[df["has_base"] & df["has_r1_or_r2"]]

    # Get unique texts and remove apostrophes
    valid_texts = df_valid["text"].drop_duplicates().str.replace("'", "", regex=False).tolist()

    return valid_texts

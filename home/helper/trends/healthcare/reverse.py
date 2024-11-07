# # imports
# import pandas as pd
# import re

# def reverse_healthcare(base, r1, r2):
#     '''
#     reverse_healthcare: Reverse queries for documents with base, r1, and r2 for all text data in Healthcare
#     return: a list containing all docs with base, r1, and r2
    
#     Parameters:
#     base: string (word)
#     r1: string (word)
#     r2: string (word)
#     '''
#     path = "home/helper/trends/healthcare/data/full.csv"

#     # load in data
#     # df=pd.read_csv(path)
#     df=pd.read_csv(path)

#     # Ensure 'text' column exists
#     if 'text' not in df.columns:
#         raise ValueError("Input CSV must contain 'text' column.")

#     # clean 
#     def clean(df):
#         '''
#         cleaning procedure for healthcare text data 
#         '''
#         # added .copy() to avoid SettingWithCopyWarning
#         # https://www.analyticsvidhya.com/blog/2021/11/3-ways-to-deal-with-settingwithcopywarning-in-pandas/
#         df=df[["text"]].copy()

#         # replace texts
#         df["text"] = df["text"].apply(lambda text: text.replace("**NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY** ", ""))
#         df["text"] = df["text"].apply(lambda text: text.replace("<BR/>", ""))
#         df["text"] = df["text"].apply(lambda text: text.replace(">", ""))
    
#         # lower and remove punctuation
#         df["clean"] = df["text"].apply(lambda text: text.lower())
#         df["clean"] = df["clean"].apply(lambda text: re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text))
#         df["tokens"] = df["clean"].apply(lambda text: text.split())
#         # tokenize
#         return df

#     # query for base -> keep if text has r1 or r2
#     def filter(tokens):
#         if base.lower() in tokens:
#             if r1.lower() in tokens or r2.lower() in tokens: 
#                 return 1
#         return 0
    
#     # cleaned df
#     text=clean(df)
#     text["valid"]=text["tokens"].apply(lambda tokens: filter(tokens))

#     # list of strings containing base with r1 or r2 that passed filter function with return of 1
#     # drop(axis=1, labels=["tokens"]) because drop_duplicates() does not work with hashables in dataframe column
#     text=text.query("valid==1").drop(axis=1, labels=["tokens"]).drop_duplicates()["text"].to_list()

#     # replacing apostrophe
#     def single(x): 
#         x.replace("\'", "")

#     # return finalized list of strings
#     return list(map(single, text))


# ----------------------------------------------

# # import pandas as pd
# import polars as pd
# import re

# def reverse_healthcare(base, r1, r2):
#     '''
#     Reverse queries for documents containing the base word and either r1 or r2 from Healthcare data.
#     Returns a list of unique documents matching the criteria.

#     Parameters:
#     base: string (word)
#     r1: string (word)
#     r2: string (word)
#     '''
#     path = "home/helper/trends/healthcare/data/full.csv"

#     # Load data
#     df = pd.read_csv(path)

#     # Ensure 'text' column exists
#     if 'text' not in df.columns:
#         raise ValueError("Input CSV must contain 'text' column.")

#     # Clean the text
#     df = df[['text']].copy()
#     df['text'] = df['text'].str.replace("**NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY** ", "", regex=False)
#     df['text'] = df['text'].str.replace("<BR/>", "", regex=False)
#     df['text'] = df['text'].str.replace(">", "", regex=False)
#     df['clean'] = df['text'].str.lower()
#     df['clean'] = df['clean'].str.replace(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", regex=True)

#     # Prepare regex patterns with word boundaries
#     base_pattern = r"\b" + re.escape(base.lower()) + r"\b"
#     r1_pattern = r"\b" + re.escape(r1.lower()) + r"\b"
#     r2_pattern = r"\b" + re.escape(r2.lower()) + r"\b"

#     # Check for the presence of base, r1, and r2
#     df["has_base"] = df["clean"].str.contains(base_pattern, regex=True)
#     df["has_r1_or_r2"] = df["clean"].str.contains(r1_pattern, regex=True) | df["clean"].str.contains(r2_pattern, regex=True)

#     # Filter rows where base and (r1 or r2) are present
#     df_valid = df[df["has_base"] & df["has_r1_or_r2"]]

#     # Get unique texts and remove apostrophes
#     valid_texts = df_valid["text"].drop_duplicates().str.replace("'", "", regex=False).tolist()

#     return valid_texts

# ----------------------------------------------

import polars as pl
import re

def reverse_healthcare(base, r1, r2):
    '''
    Reverse queries for documents containing the base word and either r1 or r2 from Healthcare data.
    Returns a list of unique documents matching the criteria.

    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path = "home/helper/trends/healthcare/data/full.csv"

    # Load data with correct data types
    df = pl.read_csv(path, dtypes={'facility_id': pl.Utf8})

    # Ensure 'text' column exists
    if 'text' not in df.columns:
        raise ValueError("Input CSV must contain 'text' column.")

    # Clean the text
    df = df.select('text')

    df = df.with_columns([
        pl.col('text')
        .str.replace("**NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY** ", "", literal=True)
        .str.replace("<BR/>", "", literal=True)
        .str.replace(">", "", literal=True)
        .str.to_lowercase()
        .str.replace_all(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", literal=False)
        .alias('clean')
    ])

    # Prepare regex patterns with word boundaries
    base_pattern = r"\b" + re.escape(base.lower()) + r"\b"
    r1_pattern = r"\b" + re.escape(r1.lower()) + r"\b"
    r2_pattern = r"\b" + re.escape(r2.lower()) + r"\b"

    # Check for the presence of base, r1, and r2
    df = df.with_columns([
        pl.col('clean').str.contains(base_pattern).alias('has_base'),
        (pl.col('clean').str.contains(r1_pattern) | pl.col('clean').str.contains(r2_pattern)).alias('has_r1_or_r2')
    ])

    # Filter rows where base and (r1 or r2) are present
    df_valid = df.filter(pl.col('has_base') & pl.col('has_r1_or_r2'))

    # Get unique texts and remove apostrophes
    valid_texts = df_valid.select(
        pl.col('text').str.replace("'", "", literal=True).alias('text')
    ).unique()

    return valid_texts['text'].to_list()

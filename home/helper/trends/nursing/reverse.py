"""
FILE DESCRIPTION: reverse.py

This script performs reverse queries on nursing home inspection data to retrieve documents
containing specified base terms and related terms. It filters inspection reports based on
whether they contain a base term along with at least one of two related terms. The script
cleans and tokenizes the data, applies the filter, and returns a list of relevant documents.

The data is assumed to be located in the 'data/' directory within the BASE_DIR.
"""

# # imports
# import pandas as pd
# import re

# BASE_DIR = "home/helper/trends/nursing/"
# DATA_PATH = BASE_DIR + "data/full.csv"

# def reverse_nursing(base, r1, r2):
#     '''
#     reverse_nursing: Retrieves inspection reports containing a base term along with either of two related terms (r1, r2).
    
#     Parameters:
#     - base (str): Base term to search within inspection reports.
#     - r1 (str): First related term.
#     - r2 (str): Second related term.
    
#     Returns:
#     - List[str]: A list of inspection report texts that contain the base term along with either r1 or r2.
#     '''
#     # Load data
#     text = pd.read_csv(DATA_PATH)

#     # Clean and preprocess text
#     text["clean"] = text["text"].apply(lambda t: t.lower())
#     text["clean"] = text["clean"].apply(lambda t: re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", t))

#     # Tokenize the cleaned text
#     text["tokens"] = text["clean"].apply(lambda t: t.split())

#     # Filter function to find entries containing the base term and either r1 or r2
#     def filter_terms(tokens):
#         if base.lower() in tokens:
#             if r1.lower() in tokens or r2.lower() in tokens:
#                 return 1
#         return 0

#     text["valid"] = text["tokens"].apply(lambda tokens: filter_terms(tokens))

#     # Select relevant documents and remove duplicates
#     filtered_docs = text.query("valid == 1").drop(columns=["tokens", "valid"]).drop_duplicates()
#     filtered_texts = filtered_docs["text"].to_list()

#     # Remove single quotes from text entries
#     remove_apostrophe = lambda x: x.replace("'", "")

#     # Return the list of filtered documents
#     return list(map(remove_apostrophe, filtered_texts))


import polars as pl
import re

def reverse_nursing(base, r1, r2):
    '''
    Reverse queries for inspection reports containing the base word and either r1 or r2 from Nursing Home data.
    Returns a list of unique documents matching the criteria.

    Parameters:
    base: string (word)
    r1: string (word)
    r2: string (word)
    '''
    path = "home/helper/trends/nursing/data/full.csv"

    # Load data
    df = pl.read_csv(path)

    # Ensure 'text' column exists
    if 'text' not in df.columns:
        raise ValueError("Input CSV must contain 'text' column.")

    # Clean the text
    df = df.select('text')

    df = df.with_columns([
        pl.col('text')
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

# imports
import re, nltk
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

num_alphas  = "one,two,three,four,five,six,seven,eight,nine,ten,"
rem_words = num_alphas
rem_words = rem_words.split(',')
rem_words = [stemmer.stem(t) for t in rem_words]

def rem_stop_words(example_sent):
    
    example_sent = str(example_sent.lower())
    stop_words = set(stopwords.words('english')) 

    word_tokens = word_tokenize(example_sent) 
  
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w)
            if w == "." or w == "?" or w == "!" or w == "," or w =="'" or w == "’" or w == "”" or w == ":" or w == "‘" or w == "“":
                filtered_sentence = filtered_sentence[:-2]
            filtered_sentence.append(" ")
    TreebankWordDetokenizer().detokenize(filtered_sentence)
    return(filtered_sentence) 

# Take in a string and remove punctuation, repeat lines, etc.
# RETURN: string (cleaned up)
def cleaner(text):
    text = re.sub('NOTE- TERMS IN BRACKETS HAVE BEEN EDITED TO PROTECT CONFIDENTIALITY','', text)
    text = re.sub('<BR/>',' ', text)
    text = text.lower()
    text = re.sub('[****]','',text)
    
    text = re.sub('[/%#;:!,.<>\'?\"()-\[\]]',' ',text)
    text = re.sub('[0-9*]','',text)

    text = re.sub(r'(?:^| )\w(?:$| )', ' ', text)
    
    a = nltk.pos_tag(tokenize_only(text))
    a = pd.DataFrame(a)
    a = a[a[1] == 'NN']
    text = ' '.join(a[0])
    
    return(text)

def to_lower(text):
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    re.sub(r"\S*https?:\S*", "", text)
    text = text.lower()
    #text = re.sub(, "", text)
    return(text)

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if(stemmer.stem(token) not in rem_words):
                filtered_tokens.append(token)
    return filtered_tokens

def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    stems = [e for e in stems if e not in rem_words ]

# output schema

# dataready = [ ...number of terms
#     {
#         "name": "fauci",
#         "values": [ ...number of periods
#             {
#                 "time": "1",
#                 "value": 0.2,
#             },
#             {},
#             ...
#         ]
#     },
#     {},
#     ...
# ]

def convert(terms, values):
    context = []
    
    for idx, val in enumerate(terms):
        temp = {
            "name": val,
            "values": []
        }
        
        for i, value in enumerate(values[idx]):
            temp["values"].append({"time": i+1, "value": value})    
            
        context.append(temp)
        
    return context

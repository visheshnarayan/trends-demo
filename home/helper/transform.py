import re
import pandas as pd, math
from functools import reduce

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

def update_csv(terms, values):
    df_data = {}
    df_data['time'] = [i+1 for i in range(len(values[0]))]
    for idx, term in enumerate(terms):
        df_data[term] = values[idx]

    try:
        # reating dataframe
        df = pd.DataFrame(df_data)

        # saving the dataframe
        df.to_csv('./home/static/csv/graph-data.csv', header=True, index=False)

        return "success"
    except:
        return "failure"

def graph_dict(values, name, base, terms, labels):
    Xval = len(labels)+1
    max_val = max(map(max, values))
    Yval = math.ceil(max_val*10)/10 + 0.2 

    return {
        "rangeX": Xval,
        "rangeY": Yval,
        "name" : name,
        "base_term": base,
        "rel_terms": terms,
        "period_labels": labels,
    }

# def sor_doc(strs, base, rel1, rel2):
def reverse_doc(strs, base, rel1, rel2):
    docs = []
    
    for doc in strs:
        sub = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", doc)
        clean = list(sub.lower().split())
        
        base = base.lower()
        r1 = rel1.lower()
        r2 = rel2.lower()
        
        pos_base = clean.index(base) if base in clean else -1
        pos_r1 = clean.index(r1) if r1 in clean else -1
        pos_r2 = clean.index(r2) if r2 in clean else -1
        
        pos = [pos_base, pos_r1, pos_r2]
        
        docs.append([doc, pos])

    # lamda function to sort according to positions
    zero_floor = lambda x: 0 if x > 0 else x
    sort_key = lambda x: (zero_floor(x[1][0]), zero_floor(x[1][1]), zero_floor(x[1][2]))
    
    docs.sort(key=sort_key, reverse=True)

#     return docs

# def reverse_doc(strs, base, rel1, rel2):
#     docs = sort_doc(strs, base, rel1, rel2)

#     print(docs)

    rev = {
        "base": base,
        "rel1": rel1,
        "rel2": rel2,
        "docs": docs,
    }

    return rev

def common_terms(mat):
    return list(reduce(lambda i, j: i & j, (set(x) for x in mat)))

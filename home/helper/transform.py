import pandas as pd

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

def graph_dict(X, Y, name, base, terms, labels):
    return {
        "rangeX": X,
        "rangeY": Y,
        "name" : name,
        "base_term": base,
        "rel_terms": terms,
        "period_labels": labels,
    }


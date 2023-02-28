import re, os, json, pandas as pd
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from . import models, forms

from home.helper.trends.nyt.generate import gen_nyt_trends
# from home.helper.trends.nyt import words

# TODO : Add urls for generic and elements.html and resolve their assets into static as well

# Create your views here.
def index(req):
    name = "nyt"
    base_term = "race"
    rel_terms = ["state", "government", "new", "sports"]

    labels, dataready, values = gen_nyt_trends(base_term, rel_terms)

    
    # TODO : create function to create and save csv
    # TODO : create new endpoint to handle updation without reloading data
    # TODO : remove old code to generate dataready
    df_data = {}
    df_data['time'] = [i+1 for i in range(len(values[0]))]
    for idx, term in enumerate(rel_terms):
        df_data[term] = values[idx]
    print(df_data)
    df = pd.DataFrame(df_data)
    print(df)

    # saving the dataframe
    df.to_csv('./home/static/csv/graph-data.csv', header=True, index=False)
    
    # TODO : generate ranges (X & Y)
    context = {
        "context": {
            "graph": {
                "rangeX": 7,
                "rangeY": 1.2,
                "name" : name,
                "base_term": base_term,
                "rel_terms": rel_terms,
                "period_labels": labels,
                # "dataready": dataready,
            },
            "form": forms.TrendForm()
        }
    }

    return render(req, 'index.html', context)

def graph_update(req):
    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.TrendForm(req.POST)

        # check for django form validity
        if form.is_valid():
            # print(form.cleaned_data)

            # loop through a python dict and add all vales to a list whose key matces a substring?
            terms = []
            for k,v in {key: value for key, value in form.cleaned_data.items() if key.startswith('rel')}.items():
                terms.append(str(v))

            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            # COMMENT : Add more models here
            if name == 'nyt':
                labels, dataready, values = gen_nyt_trends(base_term, rel_terms)

            # TODO : create function to create and save csv
            # TODO : create new endpoint to handle updation without reloading data
            # TODO : remove old code to generate dataready
            df_data = {}
            df_data['time'] = [i+1 for i in range(len(values[0]))]
            for idx, term in enumerate(rel_terms):
                df_data[term] = values[idx]
            print(df_data)
            df = pd.DataFrame(df_data)
            print(df)

            # saving the dataframe
            df.to_csv('./home/static/csv/graph-data.csv', header=True, index=False)

            return JsonResponse({
                "status":"success",
                "base_term": base_term,
                "rel_terms": rel_terms,
            })

def term_autocomplete(req, model_type):
    if req.GET.get('q'):
        if model_type == 'nyt':
            BASE_DIR = "./home/helper/trends/nyt/"
        # COMMENT : Add more models here
        # elif model_type == 'healthcare':
        #     BASE_DIR = "./home/helper/trends/healthcare/"
        else:
            return JsonResponse([], safe=False)
            
        f = open(BASE_DIR + "words.json")
        data = json.load(f)["common"]

        letter = str(req.GET['q']).lower()
        subset = [i for i in data if i.lower().startswith(letter)]

        return JsonResponse(subset, safe=False)
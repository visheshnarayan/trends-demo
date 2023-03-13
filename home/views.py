import json, pandas as pd, math
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from . import forms

# importing helper functions
from home.helper.transform import update_csv, graph_dict

# COMMENT : Import trends here
from home.helper.trends.nyt.generate import gen_nyt_trends
from home.helper.trends.healthcare.generate import gen_healthcare_trends

# Function to get initial data
def init():
    name = "nyt"
    base = "race"
    terms = ["state", "government", "news", "sports"]

    return name, base, terms

# Create your views here.
def index(req):
    # initialize model
    name, base_term, rel_terms = init()

    # get values of terms and y-axis labels
    labels, values = gen_nyt_trends(base_term, rel_terms)

    # update values in the graph data csv 
    update_csv(rel_terms, values)
    
    # Context dict to send to page
    context = {
        "context": {
            "graph": graph_dict(values, name, base_term, rel_terms, labels),
            "form": forms.TrendForm()
        }
    }

    return render(req, 'index.html', context)

def generic(req):
    return render(req, 'generic.html')

def elements(req):
    return render(req, 'elements.html')

def graph_update(req):
    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.TrendForm(req.POST)

        # check for django form validity
        if form.is_valid():
            # loop through a python dict and add all vales to a list whose key matces a substring?
            terms = []
            for k,v in {key: value for key, value in form.cleaned_data.items() if key.startswith('rel')}.items():
                terms.append(str(v))

            # received data
            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            # COMMENT : Add more models here
            if name == 'nyt':
                labels, values = gen_nyt_trends(base_term, rel_terms)
            elif name == 'healthcare':
                labels, values = gen_healthcare_trends(base_term, rel_terms)

            # updating the data stored in the graph csv
            update_csv(rel_terms, values)

            return JsonResponse({
                "status":"success",
                "code": 200,
                "graph": graph_dict(values, name, base_term, rel_terms, labels),
            })

def term_autocomplete(req, model_type):
    if req.GET.get('q'):
        if model_type == 'nyt':
            BASE_DIR = "./home/helper/trends/nyt/"
        # COMMENT : Add more models here
        elif model_type == 'healthcare':
            BASE_DIR = "./home/helper/trends/healthcare/"
        else:
            return JsonResponse([], safe=False)
            
        f = open(BASE_DIR + "words.json")
        data = json.load(f)["common"]

        letter = str(req.GET['q']).lower()
        subset = [i for i in data if i.lower().startswith(letter)]

        return JsonResponse(subset, safe=False)
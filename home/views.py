# imports
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

# COMMENT : Import Reverse logic here
from home.helper.trends.nyt.reverse import reverse_nyt
from home.helper.trends.healthcare.reverse import reverse_healthcare

# TODO : add proper descripion to all functions and methods and files

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
            "trendForm": forms.TrendForm(),
            "revData": {
                "base": "race",
                "rel1": "government", 
                "rel2": "news",
                # TODO : update docs data structure to also include position data of terms
                "docs": [
                    "In College Football, No Player Escapes the Eye of the Strength Coach/tHead coaches and players emphasize the importance of the strength coach, and salaries for the position at top college football programs are growing.",
                    "Where CPR on a Boy Is Time Wasted: U.S. Doctors Recall Aleppo’s Horrors/tThree American doctors provided a personal perspective on the deepening emergency in a Syrian city where local doctors have grown weary of the bloodshed.",
                    "Israel's Benjamin Netanyahu, Still a Step Ahead of Scandals, Faces a New Inquiry/tThe new attorney general says he will take a hard line, but Mr. Netanyahu has shown he can slip away from accusations with Teflon-coated ease.",
                    "Russia's Acres, if Not Its Locals, Beckon Chinese Farmers/tWith farmland in China scarce, migrants are crossing the border to lease large, unused tracts in the Far East, where many residents grumble about their presence and hard work.",
                    "Exaggerator Storms Down the Stretch to Win the Haskell Invitational/tOn a sloppy track, Nyquist, the Kentucky Derby winner, faded to fourth in a field of six."
                ]
            },
            "revForm": forms.ReverseForm(),
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

# TODO : finish thsi method
def reverse(req):
    # if request method is POST
    if req.method == 'POST':
        # submitted info
        form = forms.ReverseForm(req.POST)

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

            # TODO : add reverse logic
            # # COMMENT : Add more models here
            if name == 'nyt':
                rev_data = reverse_nyt(base_term, rel_terms[0], rel_terms[1], 'aug20')
            elif name == 'healthcare':
                # example:
                #   base: diseases
                #   rel1:  infections
                #   rel1:  cleaning
                rev_data = reverse_healthcare(base_term, rel_terms[0], rel_terms[1], '2019')

            print(rev_data)

            # # updating the data stored in the graph csv
            # update_csv(rel_terms, values)

            # return JsonResponse({
            #     "status":"success",
            #     "code": 200,
            #     "graph": graph_dict(values, name, base_term, rel_terms, labels),
            # })

            # return JsonResponse({
            #     "status":"success",
            #     "code": 200,
            # })

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
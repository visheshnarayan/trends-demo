"""
FILE DESCRIPTION: views.py

This file contains the views for a Django project to generate and display trends analysis 
based on various datasets (NYT, healthcare, nursing). It includes functions for rendering 
pages, updating trend graphs, handling reverse queries, and providing term autocomplete 
suggestions based on the selected dataset.

Functions:
- init: Initializes default model parameters for NYT trends.
- index: Renders the main index page with default trend data.
- method: Renders the methodology page.
- about: Renders the about-us page.
- graph_update: Updates the trend graph based on user-selected terms and dataset.
- reverse: Handles reverse query requests, filtering documents by specified terms.
- term_autocomplete: Provides autocomplete suggestions for terms based on selected model.
"""

# imports
import json
from django.shortcuts import render
from django.http import JsonResponse
from . import forms

# importing helper functions
from home.helper.transform import update_csv, graph_dict, reverse_doc

## TRENDS
# NYT
from home.helper.trends.nyt.generate import gen_nyt_trends
from home.helper.trends.nyt.reverse import reverse_nyt
# Healthcare
from home.helper.trends.healthcare.generate import gen_healthcare_trends
from home.helper.trends.healthcare.reverse import reverse_healthcare
# Nursing
from home.helper.trends.nursing.generate import gen_nursing_trends
from home.helper.trends.nursing.reverse import reverse_nursing

# Function to get initial data
def init():
    """
    Initializes the default parameters for NYT trends.

    Returns:
    - name (str): Default dataset name ('nyt').
    - base (str): Default base term ('race').
    - terms (List[str]): Default related terms.
    - docs (List[str]): Initial list of documents filtered by the reverse query function.
    """
    name = "nyt"
    base = "race"
    terms = ["state", "government", "news", "sports"]

    # Retrieve initial documents for NYT trends
    docs = reverse_nyt(base, terms[0], terms[1])

    return name, base, terms, docs

# Create your views here.
def index(req):
    """
    Renders the main index page with default trend data.

    Parameters:
    - req: HTTP request object.

    Returns:
    - HttpResponse: Rendered index.html page with initial context data for NYT trends.
    """
    # initialize model
    name, base_term, rel_terms, rev_data = init()

    # get values of terms and y-axis labels
    labels, values = gen_nyt_trends(base_term, rel_terms)

    # update values in the graph data csv
    update_csv(rel_terms, values)
    
    # Context dict to send to page
    context = {
        "context": {
            "graph": graph_dict(values, name, base_term, rel_terms, labels),
            "trendForm": forms.TrendForm(),
            "revData": reverse_doc(rev_data, base_term, rel_terms[0], rel_terms[1]),
            "revForm": forms.ReverseForm(),
        }
    }

    return render(req, 'index.html', context)

def method(req):
    """
    Renders the methodology page.

    Parameters:
    - req: HTTP request object.

    Returns:
    - HttpResponse: Rendered method.html page.
    """
    return render(req, 'method.html')

def about(req):
    """
    Renders the about-us page.

    Parameters:
    - req: HTTP request object.

    Returns:
    - HttpResponse: Rendered about-us.html page.
    """
    return render(req, 'about-us.html')

def graph_update(req):
    """
    Updates the trend graph based on user-selected terms and dataset.

    Parameters:
    - req: HTTP POST request containing the form data with selected model type, base term,
      and related terms.

    Returns:
    - JsonResponse: JSON response with updated graph data or an error message if the request is invalid.
    """
    if req.method == 'POST':
        form = forms.TrendForm(req.POST)

        if form.is_valid():
            terms = [str(v) for k, v in form.cleaned_data.items() if k.startswith('rel')]

            # received data
            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = terms

            # Generate trends based on selected model
            if name == 'nyt':
                labels, values = gen_nyt_trends(base_term, rel_terms)
            elif name == 'healthcare':
                labels, values = gen_healthcare_trends(base_term, rel_terms)
            elif name == 'nursing':
                labels, values = gen_nursing_trends(base_term, rel_terms)

            # updating the data stored in the graph csv
            update_csv(rel_terms, values)

            return JsonResponse({
                "status": "success",
                "code": 200,
                "graph": graph_dict(values, name, base_term, rel_terms, labels),
            })

def reverse(req):
    """
    Handles reverse query requests, filtering documents by specified base and related terms.

    Parameters:
    - req: HTTP POST request containing form data with model type, base term, and related terms.

    Returns:
    - JsonResponse: JSON response with a list of documents that contain the specified terms.
    """
    if req.method == 'POST':
        form = forms.ReverseForm(req.POST)

        if form.is_valid():
            # received data
            name = form.cleaned_data["model_type"]
            base_term = form.cleaned_data["base_term"]
            rel_terms = [str(v) for k, v in form.cleaned_data.items() if k.startswith('rel')]

            print("===> Reverse Query:")
            print(name, base_term, rel_terms)


            # Reverse query based on selected model
            if name == 'nyt':
                # nyt race ['state', 'government']
                rev_data = reverse_nyt(base_term, rel_terms[0], rel_terms[1])
                ## rev_data = ["doc1", "doc2", "doc3"]
            elif name == 'healthcare':
                # healthcare healthcare ['medicine', 'cost']
                rev_data = reverse_healthcare(base_term, rel_terms[0], rel_terms[1])
            elif name == 'nursing':
                # nursing patient ['doctor', 'family']
                rev_data = reverse_nursing(base_term, rel_terms[0], rel_terms[1])

            print(rev_data)

            return JsonResponse({
                "status": "success",
                "code": 200,
                "revData": reverse_doc(rev_data, base_term, rel_terms[0], rel_terms[1]),
            })

def term_autocomplete(req, model_type):
    """
    Provides autocomplete suggestions for terms based on the selected model.

    Parameters:
    - req: HTTP request object with query parameter 'q' for autocomplete term.
    - model_type (str): Type of the model (e.g., 'nyt', 'healthcare', 'nursing').

    Returns:
    - JsonResponse: JSON response with a list of autocomplete suggestions.
    """
    if req.GET.get('q'):
        if model_type == 'nyt':
            BASE_DIR = "./home/helper/trends/nyt/"
        elif model_type == 'healthcare':
            BASE_DIR = "./home/helper/trends/healthcare/"
        elif model_type == 'nursing':
            BASE_DIR = "./home/helper/trends/nursing/"
        else:
            return JsonResponse([], safe=False)
            
        with open(BASE_DIR + "words.json") as f:
            data = json.load(f)["common"]

        letter = str(req.GET['q']).lower()
        subset = [i for i in data if i.lower().startswith(letter)]

        return JsonResponse(subset, safe=False)

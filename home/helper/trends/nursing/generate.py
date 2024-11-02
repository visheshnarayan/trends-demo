"""
FILE DESCRIPTION: generate.py

This script generates trend data for nursing home inspection reports by computing similarity scores
between a base term and a set of related terms across multiple Word2Vec models. Each model represents
a different time period (e.g., 'jan23') and is dynamically loaded from the 'models/' directory.

The trends are derived based on cosine similarity scores, providing insights into how related terms
vary in relation to the base term across different time periods.
"""

# imports
from gensim.models import Word2Vec
from scipy.spatial import distance
import os

BASE_DIR = "./home/helper/trends/nursing/"
MODELS_DIR = os.path.join(BASE_DIR, "models/")

def gen_nursing_trends(base_term, rel_terms):
    """
    Generates trend data by calculating cosine similarity scores between a base term and multiple related terms
    across multiple Word2Vec models. Each model corresponds to a different time period, allowing trend analysis
    over time.

    Parameters:
    - base_term (str): The base word to calculate similarity against.
    - rel_terms (List[str]): A list of related terms for which cosine similarity scores will be calculated
      in relation to the base term.

    Returns:
    - labels (List[str]): List of time period labels derived from the model filenames (e.g., 'jan23').
    - values (List[List[float]]): A 2D list where each inner list contains similarity scores for one related term
      across all models (time periods).

    Notes:
    - If a term is missing in any model, a maximum cosine distance of 1.0 is assigned by default for that model.
    """
    # Dynamically load model files from the models directory
    model_files = sorted([f for f in os.listdir(MODELS_DIR) if f.endswith(".model")])
    labels = [file.split('.')[0] for file in model_files]
    
    # Load Word2Vec models
    models = [Word2Vec.load(os.path.join(MODELS_DIR, file)) for file in model_files]

    # Get similarity scores
    values = []
    
    for rel in rel_terms:
        rel_scores = []
        for model in models:
            try:
                score = distance.cosine(model.wv[base_term], model.wv[rel])
                rel_scores.append(score)
            except KeyError:
                # If base_term or rel term not found in model, set max distance
                rel_scores.append(1.0)
                print(f"Term '{base_term}' or '{rel}' not found in model.")
        values.append(rel_scores)

    # Return labels and similarity values
    return labels, values

# imports
from gensim.models import Word2Vec
from scipy.spatial import distance

BASE_DIR = "./home/helper/trends/nyt/"

# labels
labels = ["Jan20", "Aug20", "Dec20", "Jan21", "Aug21", "Dec21"]

def gen_nyt_trends(base_term, rel_terms):
    # load W2V models
    models = []

    for label in labels:
        models.append(Word2Vec.load(f"{BASE_DIR}models/{label}.model"))

    # get similarity scores
    values = []

    # looping through all relative terms
    for idx, rel in enumerate(rel_terms):
        # looping through all models
        vals = []
        for i, model in enumerate(models):
            try:
                vals.append(1-distance.cosine(model.wv[base_term], model.wv[rel]))
            except Exception as e:
                vals.append(-1.0)
                print(f"Term '{base_term}' or '{rel}' not found in model. Error: {e}")
        values.append(vals)

    # returning values
    return labels, values

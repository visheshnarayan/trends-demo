# imports
from gensim.models import Word2Vec
from scipy.spatial import distance

BASE_DIR = "./home/helper/trends/healthcare/"

# labels
labels = ["2016", "2017", "2018", "2019"]

def gen_healthcare_trends(base_term, rel_terms):
    # loading models
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
                # vals.append(1-distance.cosine(model.wv[base_term], model.wv[rel]))
                cos_dist = distance.cosine(model.wv[base_term], model.wv[rel])
                norm_sim = 1 - (cos_dist / 2)
                vals.append(norm_sim)
            except Exception as e:
                vals.append(-1.0)
                print(f"Term '{base_term}' or '{rel}' not found in model. Error: {e}")
        values.append(vals)

    # returning values
    return labels, values
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
        models.append(Word2Vec.load(BASE_DIR + f"models/{label}.model"))

    # get similarity scores
    values = []

    # looping through all relative terms
    for idx, rel in enumerate(rel_terms):
        # looping through all models
        vals = []
        for i, model in enumerate(models):
            try:
                vals.append(distance.cosine(model.wv[base_term], model.wv[rel]))
            except Exception as e:
                vals.append(1.0)
                print(f"Exception occured in model: {model}, number: {i}\nbase term: {base_term}, relative term: {rel}")
        values.append(vals)

    # returning values
    return labels, values
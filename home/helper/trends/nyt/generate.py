# imports
from gensim.models import Word2Vec
from scipy.spatial import distance

from home.helper.process import convert

BASE_DIR = "./home/helper/trends/nyt/"

# labels
labels = ["jan20", "aug20", "dec20", "jan21", "aug21", "dec21"]

def gen_nyt_trends(base_term, rel_terms):
    # load W2V models
    models = []

    models.append(Word2Vec.load(BASE_DIR + "models/jan20.model"))
    models.append(Word2Vec.load(BASE_DIR + "models/aug20.model"))
    models.append(Word2Vec.load(BASE_DIR + "models/dec20.model"))

    models.append(Word2Vec.load(BASE_DIR + "models/jan21.model"))
    models.append(Word2Vec.load(BASE_DIR + "models/aug21.model"))
    models.append(Word2Vec.load(BASE_DIR + "models/dec21.model"))

    # get similarity scores
    values = []

    # looping through all relative terms
    for idx, rel in enumerate(rel_terms):
        # looping through all models
        vals = []
        for i, model in enumerate(models):
            # TODO : Add logic for if base term does not exist
            # TODO : add logic to handle if term not present

            try:
                vals.append(distance.cosine(model.wv[base_term], model.wv[rel]))
            except Exception as e:
                if not vals:
                    vals.append(1.0)
                else:
                    vals.append(vals[-1])

                print(f"Exception occured in model: {model}, number: {i}\nbase term: {base_term}, relative term: {rel}")
        values.append(vals)

    # creating dataready
    dataready = convert(rel_terms, values)

    # returning values
    return labels, dataready, values


    
    



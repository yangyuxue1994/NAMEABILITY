import numpy as np
import pandas as pd
import sys
from gensim.models import word2vec
from itertools import combinations


def word2VecSimilarity(model,w1,w2):
    print ('in method 1')
    try:
        return model.similarity(w1,w2)
    except KeyError:
        return 0
    except:
        return 0

def get_words(words_file, model):
    df = pd.read_csv(words_file, header=[0,1])
    trials = [str(i) for i in df.columns.levels[0]]

    w2vSimilarity = {}
    for trial in trials:
        # one trial df 'word1' 'word2'
        dt = df[trial]
        dt = dt.dropna(how='any')
        pairs = list(zip(dt['word1'], dt['word2']))
        similarity = []
        for p in pairs:
            similarity.append(word2VecSimilarity(model, p[0], p[1]))
        w2vSimilarity[trial] = sum(similarity)/float(len(similarity))
    return w2vSimilarity

# main #
path  = '/Users/Cher/Documents/UW/2017LAB/Lupyan/NAMEABILITY/name/output/GoogleNews-vectors-negative300.bin'
words_file = '../output/word_pairs.csv'
model = word2vec.KeyedVectors.load_word2vec_format(path,binary=True)

get_words(words_file, model).to_csv('w2v_similarity.csv', colums=['w2v_sim'])


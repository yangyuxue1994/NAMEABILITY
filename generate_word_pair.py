import numpy as np
import pandas as pd
import sys
from gensim.models import word2vec
import nltk
from nltk.corpus import stopwords
from itertools import combinations

def get_pair():
    d=pd.read_csv('clean_output_trial.csv', header=0)
    d.applymap(str)
    problems = d.columns.values.tolist()

    s_pair = dict()
    w_pair = dict()
    ww = dict()
    for curProb in problems:
        cur_df = d[curProb].dropna(axis=0, how='any')
        sentence_pairs = list(combinations(cur_df,2))
        word_pairs = []
        word_pairs_expand = word_pairs[:]
        for cur_pair in sentence_pairs:
            words = list(get_word_pair(cur_pair)) # two sentence, s1-s2=[(x1, y1), (x2, y2)...]
            word_pairs.append(words)            # [s1-s2], [s1-s3]
            word_pairs_expand.extend(words)
        s_pair[curProb] = sentence_pairs
        w_pair[curProb] = word_pairs
        ww[curProb] = word_pairs_expand


    output = pd.DataFrame.from_dict(ww, orient = 'index').T
    output.to_csv('word_pairs_tuples.csv',index=False)

    # export non-tuple pairs
    cols = ww.keys()
    d = {k: pd.DataFrame(v, columns=['word1','word2']) for k,v in ww.items()}
    df = pd.concat(d, axis=1)
    df.to_csv('word_pairs.csv',index=False)

    return output

def get_word_pair(sentence_pair):
    s1 = sentence_pair[0]
    s2 = sentence_pair[1]

    words1 = nltk.word_tokenize(s1)
    words2 = nltk.word_tokenize(s2)

    return [(w1, w2) for w1 in words1 for w2 in words2]

get_pair()










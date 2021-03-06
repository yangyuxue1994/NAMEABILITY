import numpy as np
import pandas as pd
import sys
#from gensim.models import word2vec
import nltk
#nltk.download('punkt')
from nltk.corpus import stopwords
from itertools import combinations

def get_pair(file):
    d=pd.read_csv(file, header=0)
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

    # manipulate particular output you want
    export_word_tuples = False
    export_word = True
    export_sentence = False

    # export tuple pairs
    if export_word_tuples:
        print ('export  word_tuple!')
        output.to_csv('word_pairs_tuples.csv',index=False)

    # export non-tuple pairs
    if export_word:
        print ('export word pairs!')
        cols = ww.keys()
        d = {k: pd.DataFrame(v, columns=['word1','word2']) for k,v in ww.items()}
        df = pd.concat(d, axis=1)
        df.to_csv('../output/word_pairs.csv',index=False)

    if export_sentence:
        print ('export sentence pairs!')
        output = pd.DataFrame.from_dict(ww, orient = 'index').T
        output.to_csv('../output/word_pairs_tuples.csv',index=False)

        
        s_cols = s_pair.keys()
        s_d = {k: pd.DataFrame(v, columns=['s1','s2']) for k,v in s_pair.items()}
        s_df = pd.concat(s_d, axis=1)
        s_df.to_csv('../output/sentence_pairs.csv',index=False)

    # only return word pairs for later use
    output = pd.DataFrame.from_dict(ww, orient = 'index').T
    return output

def get_word_pair(sentence_pair):
    s1 = sentence_pair[0]
    s2 = sentence_pair[1]

    words1 = nltk.word_tokenize(s1)
    words2 = nltk.word_tokenize(s2)

    return [(w1, w2) for w1 in words1 for w2 in words2]


####################### main #######################
clean_trial_path = '../output/clean_output_trial.csv'
get_pair(clean_trial_path)










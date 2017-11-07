import sys, numpy
sys.path.append('../src')
import data_io, params, SIF_embedding

from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np
from itertools import combinations


def get_cos(embedding, sentences):
    pairs = list(combinations(embedding,2))
    print 'num of paris', len(pairs)
    for i in range(len(pairs)):
        emb1 = pairs[i][0]
        emb2 = pairs[i][1]
        inn = (emb1 * emb2).sum()
        emb1norm = numpy.sqrt((emb1 * emb1).sum())
        emb2norm = numpy.sqrt((emb2 * emb2).sum())
        score = inn / emb1norm / emb2norm
        cos = 1-score
        print get_sentence_pair(sentences,i), 'cos=', cos # 1=same; low cos means high agreement; high cos means low agreement
        if score<0:
            print 'negative score: ', cos, get_sentence_pair(sentences,i)


def get_sentence_pair(sentences, i):
    pairs = list(combinations(sentences,2))
    return pairs[i]



# input
wordfile = '../data/newVectors.txt' # word vector file, can be downloaded from GloVe website
#wordfile = '..data/GoogleNews-vectors-negative300_50000_new.txt'

weightfile = '../auxiliary_data/enwiki_vocab_min200.txt' # each line is a word and its frequency
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 0 # number of principal components to remove in SIF weighting scheme
#sentences = ['this is an example sentence', 'this is another example sentence', 'red apple on the table']
#sentences = ['aklsdj alkejs alksej dc', 'eiwuouaoudsoi cz ans damhse']
#sentences = ['black dot attached line', 'dot line', 'dot line', 'dot line', 'dot line', 'dot line', 'dot placed line', 'dot', 'dot line', 'dot line', 'position dot', 'dot line', 'dot line', 'dot line', 'along line', 'circle line', 'black dot line', 'dot line', 'dot line', 'dot line', 'dot line', 'point line']
#sentences =  ['shape sharper angles', 'shape perfect trapezoid', 'shape', 'dot placement', 'weird', 'dot shorter base trapezoid', 'dot left side', 'position', 'parallels', 'looks weird', 'point middle', 'left dot', 'trapezoid rhombus', 'white dot isnt centered', 'dot far away short line', 'different shapoe', 'dot one side', 'dot close larger base', 'position']

sentences = ['white dot centered', 'white dot centered']


# load word vectors
(words, We) = data_io.getWordmap(wordfile)
# load word weights
word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'
weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word
# load sentences
x, m = data_io.sentences2idx(sentences, words) # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
w = data_io.seq2weight(x, m, weight4ind) # get word weights

# set parameters
params = params.params()
params.rmpc = rmpc
# get SIF embedding
embedding = SIF_embedding.SIF_embedding(We, x, w, params) # embedding[i,:] is the embedding for sentence i

## TEST
get_cos(embedding,sentences)


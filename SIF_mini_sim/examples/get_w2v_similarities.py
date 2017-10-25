import numpy as np
import pandas as pd
import sys
from gensim.models import word2vec
from itertools import combinations


#googleNews = word2vec.KeyedVectors.load_word2vec_format('/Users/glupyan/Downloads/word2vecstuff/GoogleNews-vectors-negative300.bin',binary=True)

############# word2vec #############
googleNews = word2vec.KeyedVectors.load_word2vec_format('/Users/Cher/Documents/UW/2017LAB/Lupyan/NAMEABILITY/name5/GoogleNews-vectors-negative300.bin', binary=True)
####################################

#wiki = word2vec.Word2Vec.load_word2vec_format('/Users/glupyan/Downloads/word2vecstuff/wiki.en.vec',binary=False)
#googleNews = word2vec.Word2Vec.load_word2vec_format('/Users/glupyan/Downloads/word2vecstuff/GoogleNews-vectors-negative300_50000.txt',binary=False)
#wiki = word2vec.Word2Vec.load_word2vec_format('/Users/glupyan/Downloads/word2vecstuff/wiki.en_50000.txt',binary=False)

def word2VecSimilarity(model,w1,w2):
    try:
        return model.similarity(w1,w2)
    except KeyError:
        return 'NA'
    except:
        return 'NA'

filename = sys.argv[1]
(word1,word2) = (sys.argv[2], sys.argv[3])

wordData = pd.read_csv(filename)
wordData['similarity_news'] = [word2VecSimilarity(googleNews,w1,w2) for w1,w2 in zip(list(wordData[word1]),list(wordData[word2]))]
#wordData['similarity_wiki'] = [word2VecSimilarity(wiki,w1,w2) for w1,w2 in zip(list(wordData[word1]),list(wordData[word2]))]

pd.DataFrame(wordData).to_csv(filename + "_vec2word"+ "_withSimilarities.txt")

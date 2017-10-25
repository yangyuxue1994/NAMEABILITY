import numpy as np
import pandas as pd
import sys
from gensim.models import word2vec
from itertools import combinations

#from gensim.models import KeyedVectors
#from threading import Semaphore
#model = KeyedVectors.load('/Users/Cher/Documents/UW/2017LAB/Lupyan/NAMEABILITY/name_SemSim/GoogleNews-vectors-negative300.bin.gz', mmap='r')
#model.syn0norm = model.syn0  # prevent recalc of normed vectors
#model.most_similar('stuff')  # any word will do: just to page all in
#Semaphore(0).acquire()  # just hang until process killed


def word2VecSimilarity(model,w1,w2):
    print ('in method 1')
    try:
        return model.similarity(w1,w2)
    except KeyError:
        return 'NA'
    except:
        return 'NA'

## todo: get two lists of word pair [w1,...][w2...]
def extract_word_pair(filename, trial):
    print ('in method 2')
    df = pd.read_csv(filename, header=0)
    words = df[trial].dropna()   # get particular trial
    word_pairs = words.values.tolist()
    print ('test 1!!!!!!!!!!')
    print len(word_pairs) # word_pairs = [(w1, w2), (w1, w2)...] 1315 tuples in list
    words1 = []
    words2 = []
    for word_pair in word_pairs:
        word_pair = word_pair.replace("'", "")
        word_pair = tuple(map(str, word_pair[1:-1].split(',')))
#        print type(word_pair)
#        print (word_pair)
        words1.append(word_pair[0])
        words2.append(word_pair[1])
    wordData = pd.DataFrame({'word1': words1, 'word2': words2})
    wordData.to_csv('try.csv', index = False)
    return wordData

############### main ################
print ('here 0!!!!!!!!!')

#filename = sys.argv[1]
#(word1,word2) = (sys.argv[2], sys.argv[3])
filename = 'word_pairs.csv'
(word1,word2) = 'word1', 'word2'

#comment: python get_word2vec_similarities.py wordPairs.csv word1 word2
wordData = extract_word_pair(filename, 'Transformation-rotation (34)')
#wordData = pd.read_csv(filename)
print ('here 1!!!!!!!!!')

googleNews = word2vec.KeyedVectors.load_word2vec_format('/Users/Cher/Documents/UW/2017LAB/Lupyan/NAMEABILITY/name_SemSim/GoogleNews-vectors-negative300.bin.gz',binary=False)
#googleNews.init_sims(replace=True)
#model.save('save_GoogleNews-vectors-gensim-normed.bin')
#model = word2vec.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = False)


print ('here 2!!!!!!!!!')

#Word2Vec.load('bio_word',mmap='r')

wordData['similarity_news'] = [word2VecSimilarity(googleNews,w1,w2) for w1,w2 in zip(list(wordData[word1]),list(wordData[word2]))]
print ('here 3!!!!!!!!!')

pd.DataFrame(wordData).to_csv(filename + "_withSimilarities.txt")




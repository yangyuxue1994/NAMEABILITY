import sys, numpy
sys.path.append('../src')
import data_io, params, SIF_embedding
from scipy.spatial.distance import cosine
import pandas as pd
import numpy as np
from itertools import combinations



'''
    this function is to drop any na in data
    '''
def dropna(dict):
    for k,v in dict.items():
        v[:] = [i for i in v if isinstance(i, basestring) ]
    return dict

'''
    this function import sentence file and return a dictionary for each trial with sentences
    '''
def extract_sentences(filename):
    #    print 'from clean output file'
    df = pd.read_csv(filename, header=0)
    df.applymap(str)
    sentence_dict = dropna(pd.DataFrame.to_dict(df, orient='list'))
    return sentence_dict

def get_embs(sentences, params):
    # load word vectors
    (words, We) = data_io.getWordmap(wordfile)
    # load word weights
    word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'
    weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word
    # load sentences
    x, m = data_io.sentences2idx(sentences, words) # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
    w = data_io.seq2weight(x, m, weight4ind) # get word weights
    
    # get SIF embedding
    embedding = SIF_embedding.SIF_embedding(We, x, w, params) # embedding[i,:] is the embedding for sentence i
    return embedding

'''
    This function returns a list of cos similarity for each embedding
    @param: embedding of a list of sentences
    @return:a list of cos similarity for combinations between any two senetences
    '''
def get_sif_sims(embedding):
    similarity = []
    # a list of combination of embeddings, each one is a tuple, [(emb1, emb2), (emb1, emb3)...]
    for emb_pair in list(combinations(embedding,2)):
        cos = 1-get_each_score(emb_pair)
        # print cos
        # This is to skip any negative scores
        if (cos<=1) & (cos>=0):
            similarity.append(cos)
        else:
            print 'this is a negative score', cos
    return similarity

'''
    This function is calculating a similairty between two sentence, based on their embedding vector
    @param: a tuple pair of embedding for two sentences
    @return: a single score of similarity value
    '''
def get_each_score(emb_pair):
    emb1 = emb_pair[0]
    emb2 = emb_pair[1]
    inn = (emb1 * emb2).sum()
    emb1norm = numpy.sqrt((emb1 * emb1).sum())
    emb2norm = numpy.sqrt((emb2 * emb2).sum())
    score = inn / emb1norm / emb2norm
    return score

'''
    This function return a dictionary of output
    @ return: dict, key: trial name; value: average sif_similarity
    '''
def get_ave_sims(sentence_dict, params):
    SIF_sims = {}
    for trial,sentences in sentence_dict.items():
        embedding = get_embs(sentences, params)
#        print 'sentences', sentences
        cos_similarity = get_sif_sims(embedding)    # get the cos similarity for each pair of sentence
        SIF_sims[trial] = np.mean(cos_similarity)    # get the average cos similarity for each trial
    return SIF_sims

####################################  input ####################################
print 'start main'
wordfile = '../data/glove.840B.300d.txt' # word vector file, can be downloaded from GloVe website
weightfile = '../auxiliary_data/enwiki_vocab_min200.txt' # each line is a word and its frequency
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 0 # number of principal components to remove in SIF weighting scheme
#sentences = ['this is an example sentence', 'this is another sentence that is slightly longer']


# set parameters
params = params.params()
params.rmpc = rmpc

#emb1 = embedding[0,:]
#emb2 = embedding[1,:]
#inn = (emb1 * emb2).sum()
#emb1norm = numpy.sqrt((emb1 * emb1).sum())
#emb2norm = numpy.sqrt((emb2 * emb2).sum())
#score = inn / emb1norm / emb2norm

#################################### main ####################################
inputFile = '../../output/clean_output_trial.csv'

sentence_dict = extract_sentences(inputFile)
SIF_ave_similarity = get_ave_sims(sentence_dict, params)
#print SIF_ave_similarity
print 'start export'

output = pd.DataFrame.from_dict(SIF_ave_similarity, orient='index')
output.columns = ["SIFSimilarity"]
output.to_csv('SIF_similarity_1000000.csv')


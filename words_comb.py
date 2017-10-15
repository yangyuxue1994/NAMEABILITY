import pandas as pd
import numpy as np
import difflib as diff
import string
import nltk
from nltk.corpus import stopwords
from itertools import combinations
from textblob import TextBlob
from collections import Counter

#import semantic_similarity_module
#import read_data

"""
For clean_output_* version
"""
def read_preprocessed_file(f):
    d=pd.read_csv(f, header=0)
    d.applymap(str)
    return d

def count_words_ave(col_list, trial_name):
    
    words = []
    nouns = []
    adj = []
    adv = []
    numbers = []
    for curAnswer in col_list:
        words.append(len(curAnswer.split()))
        text = TextBlob(curAnswer)
        count = Counter([j for i,j in text.tags])
        nouns.append((count['NN']+count['NNS']+count['NNPS']+count['NNPS']))
        adj.append(count['JJ']+count['JJR']+count['JJS'])
        adv.append(count['RB']+count['RBR']+count['RBS']+count['RP'])
        numbers.append(count['CD'])

    numWordsAve = sum(words)/ float(len(col_list))
    numNounsAve = sum(nouns)/ float(len(col_list))
    numAdjAve = sum(adj)/ float(len(col_list))
    numAdvAve = sum(adv)/ float(len(col_list))
    numNumbersAve = sum(numbers)/ float(len(col_list))
    return {trial_name: [numWordsAve,numNounsAve, numAdjAve,numAdvAve,numNumbersAve]}

def get_similarity(col_list, trial_name):
    col = []
    for i in col_list:
        col.append(i.split())
    sim = []
    numMatch = []
    pairs = combinations(col,2)

    for curPair in pairs:
        sim.append(diff.SequenceMatcher(None,curPair[0],curPair[1]).ratio())
        numMatch.append(numWordMatch(curPair[0],curPair[1]))
    simAve = sum(sim)/ float(len(sim))
    numMatchAve = sum(numMatch)/ float(len(numMatch))
    return {trial_name: [simAve, numMatchAve]}

# helper function for get_similarity
def numWordMatch(l1,l2):
    return len(set(l1).intersection(l2))

'''
    This function import calculated semantic similarity and no_content_prop, and combine with current df
    '''
def import_semantic_sim():
    df = pd.read_csv('semantic_similarity_output.csv', header=0, index_col=0)
    return df

def import_no_content_prop():
    df = pd.read_csv('no_content_prop.csv', header=0, index_col=0)
    return df

def import_w2v_similarity():
    df = pd.read_csv('w2vSim.csv', header=0, index_col=0)
    return df

################### between subject calculation #################
def bewteen_subject():
    df = read_preprocessed_file('clean_output_trial.csv')  # read data
    trial_names = list(df)

    ## calculate num for each column
    cols = np.transpose( df.values.tolist() )
    counts = {}
    sims = {}
    for i in range(len(cols)):
        cur_col = cols[i]# can be done in read_data.py, improve speed
        cur_counts = count_words_ave(cur_col, trial_names[i]) #trial_names[i] = trial_name
        cur_sims = get_similarity(cur_col, trial_names[i]) # {trial: [xx, xx]}
        #print cur_sims
        counts = dict(counts.items() + cur_counts.items())  # add
        sims = dict(sims.items() + cur_sims.items())
    
    # combine multiple dataframes
    df_counts = pd.DataFrame.from_dict(counts, orient='index')
    df_counts.columns = ["numWords","numNouns", "numAdj","numAdv","numNumbers"]
    df_sims = pd.DataFrame.from_dict(sims, orient='index')
    df_sims.columns = ["wordMatch", "semanticSim"]
    df_semSims = import_semantic_sim()
    df_w2vSims = import_w2v_similarity()
    df_noCon = import_no_content_prop()
    
    output_btw = pd.concat([df_counts, df_sims, df_semSims, df_w2vSims, df_noCon], axis=1, join_axes=[df_counts.index])
    output_btw.to_csv('between_subject.csv')

################### within subject calculation #################
def within_subject():
    df = read_preprocessed_file('clean_output_id.csv')  # read data
    pp_ids = list(df)

    ## calculate num for each column
    cols = np.transpose( df.values.tolist() )
    counts = {}
    for i in range(len(cols)):
        cur_col = cols[i]
        cur_counts = count_words_ave(cur_col, pp_ids[i]) #trial_names[i] = trial_name
        cur_sims = get_similarity(cur_col, pp_ids[i]) # {trial: [xx, xx]}
        counts = dict(counts.items() + cur_counts.items())  # add

    output_wint = pd.DataFrame.from_dict(counts, orient='index')
    output_wint.columns = ["numWords","numNouns", "numAdj","numAdv","numNumbers"]
    output_wint.to_csv('within_subject.csv')

########## main ############
bewteen_subject()
within_subject()

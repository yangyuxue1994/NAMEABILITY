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
        if str(curAnswer) != 'nan': # skip 'nan' response
#            print trial_name, curAnswer
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
    
    # total number of adj, total num of responses(42), average number of adj per response
    # print trial_name, numWordsAve

    return {trial_name: [numWordsAve,numNounsAve, numAdjAve,numAdvAve,numNumbersAve]}

def get_similarity(col_list, trial_name):
    col = []
    for i in col_list:
        if 'nan' not in i:  # skip 'nan'
            col.append(i.split())
    sim = []
    numMatch = []
    pairs = combinations(col,2)

    for curPair in pairs:
        sim.append(diff.SequenceMatcher(None,curPair[0],curPair[1]).ratio())
        numMatch.append(numWordMatch(curPair[0],curPair[1]))
    simAve = sum(sim)/ float(len(sim))
    numMatchAve = sum(numMatch)/ float(len(numMatch))

#    print trial_name, simAve, numMatchAve
    return {trial_name: [simAve, numMatchAve]}

# helper function for get_similarity
def numWordMatch(l1,l2):
    return len(set(l1).intersection(l2))

'''
    This function import calculated semantic similarity and no_content_prop, and combine with current df
    '''
def import_semantic_sim(trial_files):
    df = pd.read_csv(trial_files[1], header=0, index_col=0)
    return df

def import_w2v_similarity(trial_files):
    df = pd.read_csv(trial_files[2], header=0, index_col=0)
    return df

def import_sif_similarity(trial_files):
    df = pd.read_csv(trial_files[3], header=0, index_col=0)
    return df


def import_no_content_prop(trial_files):
    df = pd.read_csv(trial_files[4], header=0, index_col=0)
    return df



################### between subject calculation #################
def bewteen_subject(trial_files):
    df = read_preprocessed_file(trial_files[0])  # read clean trial data
    trial_names = list(df)
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
    df_sims.columns = ["simRatio", "wordMatch"]

    # import relevant data
    df_semSims = import_semantic_sim(trial_files)
    df_w2vSims = import_w2v_similarity(trial_files)
    df_sifSims = import_sif_similarity(trial_files)
    df_noCon = import_no_content_prop(trial_files)
    
    output_btw = pd.concat([df_counts, df_sims, df_semSims, df_w2vSims, df_sifSims, df_noCon], axis=1, join_axes=[df_counts.index])
    output_btw.to_csv('../output/between_subject.csv')

################### within subject calculation #################
def within_subject(file):
    df = read_preprocessed_file(file)  # read data
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
    output_wint.to_csv('../output/within_subject.csv')

################### main ###################

'''
    set input paths
    '''

print 'drop version'
id_file = '../output/clean_output_id.csv'
trial_files = ['../output/clean_output_trial.csv',
               '../output/semantic_similarity_output.csv',
               '../output/w2v_similarity.csv',
               '../output/SIF_similarity.csv',
               '../output/no_content_prop.csv'
               ]
raw = '../gvi_-_nameability_-_different_-_uw.csv'
# export outputs
bewteen_subject(trial_files)
within_subject(id_file)

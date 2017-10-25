import pandas as pd
import numpy as np

'''
    this function is to drop any na in data
    '''
def dropna(dict):
#    print ('in dropna method')
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


f='clean_output_trial.csv'
#extract_sentence_pairs(f, 'Geometry-Chirality-1- (38)')
extract_sentences(f)
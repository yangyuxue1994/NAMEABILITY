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
For diffResp_content * version
"""
def count(f):
    df=pd.read_excel(f, header=0)
    df.applymap(str)
    df2 = pd.DataFrame(index=df.columns,
                       columns=['numWordsAve', 'numNounsAve', 'numAdjAve', 'numAdvAve', 'numNumbersAve'])
    for (trial, responses) in df.iteritems():
        words = []
        nouns = []
        adj = []
        adv = []
        numbers = []
        for resp in responses:
            if str(resp) != 'NAN': # skip 'nan' response
                words.append(len(resp.strip().lower().split()))
                text = TextBlob(resp)
                count = Counter([j for i,j in text.tags])
                nouns.append((count['NN']+count['NNS']+count['NNPS']+count['NNPS']))
                adj.append(count['JJ']+count['JJR']+count['JJS'])
                adv.append(count['RB']+count['RBR']+count['RBS']+count['RP'])
                numbers.append(count['CD'])

        df2.loc[trial]['numWordsAve'] = sum(words)/ float(len(responses))
        df2.loc[trial]['numNounsAve'] = sum(nouns)/ float(len(responses))
        df2.loc[trial]['numAdjAve'] = sum(adj)/ float(len(responses))
        df2.loc[trial]['numAdvAve'] = sum(adv)/ float(len(responses))
        df2.loc[trial]['numNumbersAve'] = sum(numbers)/ float(len(responses))
    return df2

################### main ###################
count('diffResp_content.xlsx').to_csv('contentWordsCount.csv')
import pandas as pd
import numpy as np
import string
import csv
import nltk
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob
from collections import Counter
#import enchant


"""
For Raw Data Version: 'gvi_-_nameability_-_different_-_uw.csv'
"""

"""
    This function drop everything from raw data, and return a list of modified data
    @dataList: list, raw data before drop incomplete data, missing id data, and stop words, and no_content info
    return: dataList, list, modified data after drop
"""
def drop_data(dataList, meaningless_word):
    ## todo: drop incomplete data
    dataLIst_t = np.transpose(dataList)
    id_list = dataLIst_t[2]
    id_count = Counter(id_list)
    delete_id = []
    for id in id_count:
        if id_count[id]!=42:
            delete_id.append(id)
    
    ## todo: drop missing id data
    ## todo: drop no-sure data
    delete = []
    complete_data = []
    for data in dataList: # dataList[0]=trial; dataList[1]=resp; dataList[2]=id
        #print ('test1: ' + str(type(data[2])))
        if (type(data[2]) is float) & (data not in delete):
            delete.append(data)
        # drop 'unsure' 'sure' meainingless words
        if (meaningless_word in data[1]) & (data not in delete):
            delete.append(data)
        if (data[2] in delete_id) & (data not in delete):
            delete.append(data)
        
        #remove stop words
        data[1] = drop_stopwords(data[1])

    ## todo: drop all
    for d in delete:
        if d in dataList:
            dataList.remove(d)
    return dataList

"""
    This function is to drop stop words in one response
    res_str: str of response (raw)
    return: str of response (after drop stop words)
"""
def drop_stopwords(res_str):    # input: str;   output: str, remove punctuation
    exclude = set(string.punctuation)
    res_str = ''.join(ch for ch in res_str if ch not in exclude)

    stop = stopwords.words('english')
    res_list = res_str.lower().split()
    res_str_clean = []
    for word in res_list:
        if word not in stop:
            res_str_clean.append(word)
    return ' '.join(res_str_clean)


'''
    This function read relevant data into a dictonary
    @ param: pre-processed data
    @ return: a list of dictonary [ {participants:responses}, {trials: responses} ]
    '''
def convert_dicts(raw_data_file, meaningless_word):
    cols = ["subq_label", "response", "subjCode"]
    d=pd.read_csv(raw_data_file, header=0, usecols = cols)
    d.applymap(str)
    dataList = d.values.tolist()    #each [trial, reponse, id, no_content]

    clean_data = drop_data(dataList, meaningless_word)
   
    pp_reponse = {}
    trial_response = {}
    for curr_data in clean_data:
        id = curr_data[2]
        trial = curr_data[0]
        res = curr_data[1]

        if id in pp_reponse:
            pp_reponse[id].append(res)
        else:
            response1 = [res]
            pp_reponse[id] = response1

        # dic: key: subq_label; value: response
        if trial in trial_response:
            trial_response[trial].append(res)
        else:
            response2 = [res]   # trial dic: {trial_name: {id: [res]}}
            trial_response[trial] = response2

    return [pp_reponse, trial_response]

'''
    This function export the csv file of two dictionaries: {participants:responses}, {trials: responses}
    @ return: 
        {participants:responses} -> clean_output_id.csv
        {trials: responses} -> clean_output_trial.csv
    '''
def export_clean_data(raw_data_file, output_cleanID, output_cleanTrial, meaningless_word):
    dics = convert_dicts(raw_data_file, meaningless_word)
    dic_id = dics[0]
    dic_trial = dics[1]
    
    outputID = pd.DataFrame.from_dict(dic_id, orient='index', dtype=None).T
    outputTrial = pd.DataFrame.from_dict(dic_trial, orient='index', dtype=None).T
    
    outputID.to_csv(output_cleanID,index=False)   # each col is a ID
    outputTrial.to_csv(output_cleanTrial, index=False)    # each col is a trial


#def correct_typo(raw_file):
#    df = pd.read_csv(raw_file, header=0)
#    df.applymap(str)
#
#    for row in df.itertuples():
#        resp =  df.loc[row[0], 'response'].lower().translate(None, string.punctuation)
#        print 'test resp ', resp
#        corrected_resp = [correct_typo_helper(typo) for typo in resp]
#        df.at[row[0], 'response'] = corrected_resp
##    pd.to_csv('corrected_raw_file', index=False)
#    return df
#
#def correct_typo_helper(str):
#    d = enchant.Dict("en_US")   # check spelling
#    corrected_str = str
#    if not d.check(str):
#        print 'this is a typo: ', str, d.suggest(str)
##        corrected_str = d.suggest(str)[0]
#    return corrected_str


############## deal with no-content words ##############
'''
    This function marks meaningless reponses: 0- has content; 1- no content
    and export csv file
    @return: gvi_-_nameability_-_different_-_uw_mark.csv
    '''
def label_no_content(raw_data_file, meaningless_word):
    df = pd.read_csv(raw_data_file, header=0)
    df['no_content'] = df.apply(lambda row: int(meaningless_word in row['response']), axis=1)
    df.groupby('response')
    #df.to_csv('gvi_-_nameability_-_different_-_uw_mark.csv', index=False)
    return df

'''
    This function counts the number of no_content responses for each trial
    generate a file 'no_content_prop.csv'
    return a df with two columns: [trial_name, averageNoContent]
    '''
def count_no_content(df, output_count_no_content):
    #convert no_content column to int type
    df['no_content'] = pd.to_numeric(df['no_content'], errors='coerce')
    df_no_content1 = df.groupby(['subq_label'])['no_content'].sum()
    df_no_content2 = df.groupby(['subq_label'])['no_content'].mean()
    df_no_content = pd.concat([df_no_content1, df_no_content2], axis=1)
    # export to csv file
    df_no_content.to_csv(output_count_no_content, header=['numNoContent', 'aveNoContent'])
    return df_no_content

################### Count each response #################
'''
    This function counts number of words, number of nouns, number of adj, number of adv, and number
    of numbers for each response
    @ param: raw file
    @ return: a dataframe adding one column 'words_n_adj_adv_num'
    '''
def count_raw_response(input_rawfile, output):
    cols = ["subq_label", "response", "subjCode"]
    df=pd.read_csv(input_rawfile, header=0, usecols=cols)
    df.applymap(str)
    df['response_noStopWords']=''
    df['count_wordsNounAdjAdvNum'] = ''
    df['count_wordsNounAdjAdvNum_noStop'] = ''
    
    words = []
    nouns = []
    adj = []
    adv = []
    numbers = []
    for row in df.itertuples():       # row[0]:index row[1]:subq_label row[2]=reponse row[3]=subjCode
        raw_resp = row[2]
        raw_text = TextBlob(raw_resp)
        count = Counter([j for i,j in raw_text.tags])
        raw_numWords = len(raw_resp.split())
        raw_numNouns = count['NN']+count['NNS']+count['NNPS']+count['NNPS']
        raw_numAdj = count['JJ']+count['JJR']+count['JJS']
        raw_numAdv = count['RB']+count['RBR']+count['RBS']+count['RP']
        raw_numNumbers = count['CD']
        count_wordsNounAdjAdvNum = str(raw_numWords)+', '+str(raw_numNouns)+', '+str(raw_numAdj)+', '+str(raw_numAdv)+', '+str(raw_numNumbers)
 
        # count response removed stop words
        noStop_resp = drop_stopwords(raw_resp)
        noStop_text = TextBlob(noStop_resp)
        count = Counter([j for i,j in noStop_text.tags])
        noStop_numWords = len(noStop_resp.split())
        noStop_numNouns = count['NN']+count['NNS']+count['NNPS']+count['NNPS']
        noStop_numAdj = count['JJ']+count['JJR']+count['JJS']
        noStop_numAdv = count['RB']+count['RBR']+count['RBS']+count['RP']
        noStop_numNumbers = count['CD']
        count_wordsNounAdjAdvNum_noStop = str(noStop_numWords)+', '+str(noStop_numNouns)+', '+str(noStop_numAdj)+', '+str(noStop_numAdv)+', '+str(noStop_numNumbers)
        df.at[row[0], 'response_noStopWords'] = noStop_resp
        df.at[row[0], 'count_wordsNounAdjAdvNum'] = count_wordsNounAdjAdvNum
        df.at[row[0], 'count_wordsNounAdjAdvNum_noStop'] = count_wordsNounAdjAdvNum_noStop

    # re-organize columns and export
    df = df[['subq_label', 'subjCode', 'response', 'response_noStopWords',
             'count_wordsNounAdjAdvNum', 'count_wordsNounAdjAdvNum_noStop']]
    df.to_csv(output, index=False)
    return df


##################### main #####################
'''
    set input path and output path
    '''
raw_file = '../gvi_-_nameability_-_different_-_uw.csv'
output_count_no_content = '../output/no_content_prop.csv'
output_cleanID = '../output/clean_output_id.csv'
output_cleanTrial = '../output/clean_output_trial.csv'
output_count_raw = '../output/gvi_-_nameability_-_different_-_uw_count.csv'
meaningless_word = 'sure'

#correct_typo(raw_file)

# export 'no_content_proportion' to csv file
count_no_content(label_no_content(raw_file, meaningless_word), output_count_no_content)

# export 'clean_output_id' & 'clean_output_trial'
# remove stop words, remove meaningless words
export_clean_data(raw_file, output_cleanID, output_cleanTrial, meaningless_word)

# count each trial-subject conbination and export a file
count_raw_response(raw_file, output_count_raw)





















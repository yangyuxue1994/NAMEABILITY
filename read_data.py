import pandas as pd
import numpy as np
import string
import csv
from collections import Counter
from nltk.corpus import stopwords


"""
For Raw Data Version
"""

"""
    This function drop everything from raw data, and return a list of modified data
    @dataList: list, raw data before drop incomplete data, missing id data, and stop words, and no_content info
    return: dataList, list, modified data after drop
"""
def drop_data(dataList):
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
        if ('sure' in data[1]) & (data not in delete):
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

"""
    count the number of no_content responses for each trial
    generate a file 'no_content_prop.csv'
    return a df with two columns: [trial_name, averageNoContent]
"""
def count_no_content(df):
    #convert no_content column to int type
    df['no_content'] = pd.to_numeric(df['no_content'], errors='coerce')
    df_no_content1 = df.groupby(['subq_label'])['no_content'].sum()
    df_no_content2 = df.groupby(['subq_label'])['no_content'].mean()
    df_no_content = pd.concat([df_no_content1, df_no_content2], axis=1)
    df_no_content.to_csv('no_content_prop.csv', header=['numNoContent', 'aveNoContent'])
    return df_no_content

# READ DATA -> DICT
def convert_dicts(file):
    cols = ["subq_label", "response", "subjCode", "no_content"]
    d=pd.read_csv(file, header=0, usecols = cols)
    d.applymap(str)
    dataList = d.values.tolist()    #each [trial, reponse, id, no_content]
    
    count_no_content(d)
    clean_data = drop_data(dataList)
   
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

def import_dics():
    file = 'gvi_-_nameability_-_different_-_uw.csv' # default raw data name
    dics = convert_dicts(file)
    dic_id = dics[0]
    dic_trial = dics[1]
    
    outputID = pd.DataFrame.from_dict(dic_id, orient='index', dtype=None).T
    outputTrial = pd.DataFrame.from_dict(dic_trial, orient='index', dtype=None).T
    
    outputID.to_csv("clean_output_id.csv",index=False)   # each col is a ID
    outputTrial.to_csv("clean_output_trial.csv", index=False)    # each col is a trial


# mark reponse: 0-has content; 1-no content
def label_no_content():
    file = 'gvi_-_nameability_-_different_-_uw.csv' # default raw data name
    df = pd.read_csv(file, header=0)
    no_words = 'sure'
    df['no_content'] = df.apply(lambda row: int(no_words in row['response']), axis=1)
    df.groupby('response')
    df.to_csv('gvi_-_nameability_-_different_-_uw_mark.csv', index=False)


### main
#label_no_content()
import_dics()

























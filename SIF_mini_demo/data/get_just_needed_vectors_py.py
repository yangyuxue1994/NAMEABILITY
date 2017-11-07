import pandas as pd
import string
responses = pd.read_csv('../../gvi_-_nameability_-_different_-_uw.csv')


allResponses = responses['response'].str.cat(sep=' ').lower() #concatenate all responses into one string and lowercase
allResponses = allResponses.translate(None, string.punctuation) #remove punctuation
uniqueWords = set(allResponses.split(' ')) #note that there are some spelling mistakes.. e.g., isoscles, parallelagram


output = open('newVectors.txt','w')
with open("GoogleNews-vectors-negative300.txt",'r') as f:
    for line in f:
        if line.split(" ")[0] in uniqueWords:
            output.write(line)
output.close()



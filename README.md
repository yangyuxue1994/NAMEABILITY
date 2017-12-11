# Nameability

## Introduction:

This code is calculating the naming agreement of shape from participants' responses. 



## Steps to Calculate

#### Step1: pre-processing raw data

in pre-processing, run:

- pre_processing.py:

- generate_pair.py

  > 》》
  >
  > word_pairs.csv



#### Step2: calculate semantic similarity & word2vector similarity

in calculate folder, run:

- semantic_similarity_aw.py

- get_word2vec_similarities.py

  > 》》
  >
  > w2vSim.csv (averaged w2v_similarity per trial)
  >
  > w2v_similarity_words.csv (all word pairs and w2v_similarity for each word pair)



#### Step3: calculate SIF similarity

in SIF_mini_sim folder

> 》》SIF_similarity.csv



#### Step4: count words and combine all similarity outputs

in calculate folder, run:

- count_words.py

  >》》
  >
  >within_subject.csv
  >
  >between_subject.csv

  ​





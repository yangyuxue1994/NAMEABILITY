# NAMEABILITY
not finished yet

<h3>Important Output Files:</h3>
  <li1>1. between_subject.csv </li1>
  <li2>2. within_subject.csv</li2>



<h2>STEP1: pre-processing raw data</h2>
run read_data.py:
	- drop_data() drop incomplete data and not sure data and stop words
	- drop_stopwords() return response_string to ‘no stop word’ response_string
	- convert_dicts() read data, convert to dict format: [pp_response, trial_response]
	- import_dics() read in data, and export to ‘clean_output_id.csv’ and 'clean_output_trial.csv'
	- label_no_content() label the 'meaningless' responses as 1, 'meaningful' responses as 0
main: 
import_dics()
label_no_content()
output: 4 files:
	- clean_output_id.csv
	- clean_output_trial.csv
	- no_content_prop.csv
	- raw_mark.csv

<h2>STEP2: calculate semantic similarity</h2>
run semantic_similarity_aw.py:
1. input: clean_output_trial.csv -> output: semantic_similarity_output.csv

<h2>STEP3: calculate w2v similarity:</h2>
1. run generate_word_pair.py: pre-processing data to get pairwise word pairs
	input: clean_output_trial.csv -> output: word_pairs.csv

2. calculate w2v (running in terminal, not directly from script)
	input: word_pairs 
	-> w2vSim.csv [trialName, average similarity]
	-> (*)w2v_similarity_words.csv [all word pairs and each w2v similarity]

<h2>STEP4: count words. by trial OR by subject</h2>
run words_comb.py:
	input: clean_output_id.csv -> output: within_subject.csv
	input: clean_output_trial.csv -> output: between_subject.csv


<h3>All Output Files</h3>
1. input: clean_output_trial -> between_subject
2. input: clean_output_id -> within_subject
3. input: semantic_similarity_output 
4. input: w2v_similarity
5. input: no_content_prop

	- read_preprocessed_file()
	- count_words_ave()
	- get_similarity()
	- numWordMatch()
	
	- bewteen_subject()
	- within_subject()
	- import_semantic_sim()
	- import_no_content_prop()
	- import_w2v_similarity()



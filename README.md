# NAMEABILITY
not finished yet

<h3>Important Output Files:</h3>
  <li1>1. between_subject.csv </li1>
  <li2>2. within_subject.csv</li2>



<h2>STEP1:</h2>
run read_data.py:
	- drop_data() drop incomplete data and not sure data and stop words
	- drop_stopwords() return response_string to ‘no stop word’ response_string
	- convert_dicts() read data, convert to dict format: [pp_response, trial_response]
	- import_dics() read in data, and export to ‘clean_output’
	- label_no_content() 
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
1. input: clean_output_trial.csv -> semantic_similarity_output_test.csv

<h2>STEP3: calculate w2v similarity:</h2>
1. generate word_pairs
	input: clean_output_trial.csv -> word_pairs.csv

2. calculate w2v 
	input: word_pairs 
	-> w2vSim.csv [trialName, average sim]
	-> (*)w2v_similarity_words.csv [all word pairs and each w2v similarity]

<h2>STEP4:</h2>
run words_comb.py:


<h2>All Output Files</h2>
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



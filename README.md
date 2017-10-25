# NAMEABILITY
not finished yet

<h3>Important Output Files:</h3>
  <p>1. between_subject.csv </p>
  <p>2. within_subject.csv</p>



<h2>STEP1: pre-processing raw data</h2>
<h4>run pre_processing/pre_processing.py:</h4>
<p>
	- drop_data() drop incomplete data and not sure data and stop words</br>
	- drop_stopwords() return response_string to ‘no stop word’ response_string</br>
	- convert_dicts() read data, convert to dict format: [pp_response, trial_response]</br>
	- import_dics() read in data, and export to ‘clean_output_id.csv’ and 'clean_output_trial.csv'</br>
	- label_no_content() label the 'meaningless' responses as 1, 'meaningful' responses as 0</br>
</p>
<p>main: 
import_dics()</br>
label_no_content()</br>
output: 4 files:</br>
- clean_output_id.csv</br>
- clean_output_trial.csv</br>
- no_content_prop.csv</br>
- raw_mark.csv</br>
<p>
<h4>run pre_processing/generate_pair.py:</h4>
<p>export output/word_pairs.csv</br></p>

<h2>STEP2:calculate semantic similarity word2vector similarity</h2>
<h4>run semantic_similarity_aw.py:</h4>
	input: clean_output_trial.csv -> output: semantic_similarity_output.csv</br>

<h4>run get_word2vec_similarities.py:</h4>
	input: word_pairs.csv -> output: w2vSim.csv [trialName, average similarity]</br>
	-> (*)w2v_similarity_words.csv [all word pairs and each w2v similarity]</br>

<h2>STEP3: get SIF similarity</h2>
<h4>run SIF_mini_sim/examples/sif_embedding_0.py:</h4>
	input: clean_output_trial.csv -> output: sifSim.csv</br>

<h2>STEP4: count words and export all data: </h2>
<h4>run calculate/count_words.py:</h4>
	input: clean_output_id.csv -> output: within_subject.csv</br>
	input: clean_output_trial.csv -> output: between_subject.csv</br>


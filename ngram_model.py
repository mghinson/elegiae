import sys
import string

from ngram import NgramModel

from cltk.tokenize.sentence import TokenizeSentence
from cltk.stem.latin.j_v import JVReplacer
from cltk.stop.latin.stops import STOPS_LIST
from cltk.stem.lemma import LemmaReplacer
from tagger_client import get_POS_sentence

def remove_numbers(word):
	numbers = "0123456789"
	return ''.join(ch for ch in word if ch not in numbers);

def remove_punctuation(string):
	punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~';
	return ''.join(ch for ch in string if ch not in punctuation);

def remove_stopwords(sentence):
	stops_extra = ['ego', 'mei', 'mihi', 'me', 'tu', 'tui', 'tibi', 'te', 'meus', 
					'meo', 'meum', 'mi', 'tuus', 'tui', 'tuo', 'tuum', 'noster'];
	stops_augmented = STOPS_LIST;
	for i in range(0, len(stops_extra)):
		stops_augmented.append(stops_extra[i]);
	return [w for w in sentence if w.lower().strip() not in stops_augmented];
	#return [w for w in sentence if w.lower().strip() not in STOPS_LIST];

def lemmatize_sentence(sentence):
	lemmatizer = LemmaReplacer('latin');
	return [remove_numbers(lemmatizer.lemmatize(w)[0]) for w in sentence];

def noun_filter(possible_types):
	if not 'verb' in possible_types and not 'adverb' in possible_types:
		return True;
	return False;

def main():

	tokenizer = TokenizeSentence('latin');
	j = JVReplacer();

	whole_text = "";

	for i in range(1, len(sys.argv)):
		book = open(sys.argv[i]);
		for line in book:
			split = line.split();
			for word in split:
				if word.isdecimal():
					continue;
				whole_text += (" " + word);

	whole_text = j.replace(whole_text);
	word_dictionary = {};


	# Preprocess text

	prop_sentences = tokenizer.tokenize(whole_text);
	word2vec_input = []
	for sentence in prop_sentences:
		sentence = remove_punctuation(sentence);
		#word_dictionary = get_POS_sentence(sentence, word_dictionary);
		sentence_array = sentence.lower().split();
		sentence_array = lemmatize_sentence(sentence_array);
		sentence_array = remove_stopwords(sentence_array);
		word2vec_input.append(sentence_array);
	list_of_words = []
	for sentence in word2vec_input:
		for word in sentence:
			list_of_words.append(word)

	ngram_model = NgramModel(2, list_of_words)


	word1 = lemmatizer.lemmatize("frangenti")[0]
	word2 = lemmatizer.lemmatize("fingenti")[0]
	emendation1 = lemmatize_sentence("o prima infelix frangenti terra Prometheo")
	emendation2 = lemmatize_sentence("co prima infelix fingenti terra Prometheo")

	print("logprob of first is")
	print(ngram_model.logprob(word1, emendation1))
	print("logprob of second is")
	print(ngram_model.logprob(word2, emendation2))


	
main();
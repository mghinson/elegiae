import numpy as np
from scipy.spatial.distance import cosine 

from gensim.models import Word2Vec
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
from cltk.stop.latin.stops import STOPS_LIST
import sys

def remove_stopwords(sentence):
	stops_extra = ['ego', 'mei', 'mihi', 'me', 'tu', 'tui', 'tibi', 'te', 'meus', 
					'meo', 'meum', 'mi', 'tuus', 'tui', 'tuo', 'tuum', 'noster', 'suus', 'sui', 'suo', 'suum'];
	stops_augmented = STOPS_LIST;
	for i in range(0, len(stops_extra)):
		stops_augmented.append(stops_extra[i]);
	return [w for w in sentence if w.lower().strip() not in stops_augmented];

def remove_punctuation(string):
	punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~';
	return ''.join(ch for ch in string if ch not in punctuation);

def all_words_in_model(model, emendation):
	for word in emendation:
		if not word in model:
			return False
	return True

def detect_words_not_in_model(model, emendation):
	words_not_in_model = []
	for word in emendation:
		if not word in model:
			words_not_in_model.append(word)
	return words_not_in_model

def context_word_distance(model, context, word):
	context_vectors = [model[context_word] for context_word in context]
	context_vec_sum = np.zeros(len(context_vectors[0]))
	for i in range(len(context)):
		context_vec_sum += context_vectors[i]
	return cosine(model[word], context_vec_sum)


def detect_difference(emendations_list):
	differences = []
	base_emendation = set(emendations_list[0])
	for i in range(1, len(emendations_list)):
		emend = set(emendations_list[i])
		diff = emend.symmetric_difference(base_emendation)
		if len(diff) > 2:
			continue
		differences.append(diff)
	if len(differences) == 0:
		return []
	all_diffs = differences[0]
	for i in range(1, len(differences)):
		all_diffs = all_diffs.union(differences[i])
	return list(all_diffs)

def find_context_words(emend1, emend2):
	return [word for word in emend1 if not word in set(emend1).symmetric_difference(set(emend2))]

def model_prediction(model, context):
	context_vectors = [model[context_word] for context_word in context]
	context_vec_sum = np.zeros(len(context_vectors[0]))
	for i in range(len(context)):
		context_vec_sum += context_vectors[i]
	probs = np.dot(model.syn1, context_vec_sum)
	possibilities = len(context) + 1
	max_indices = np.argpartition(probs, -possibilities)[-possibilities:]
	min_distance = 1000
	min_word = None
	for index in max_indices:
		word = model.index2word[index]
		dis = context_word_distance(model, context, word)
		if dis < min_distance and word not in context:
			min_word = word 
			min_distance = dis
	return min_word


	"""word1 = model.index2word[max_indices[0]]
	word2 = model.index2word[max_indices[1]]
	dis1 = context_word_distance(model, context, word1)
	dis2 = context_word_distance(model, context, word2)
	if dis1 < dis2 and word1 not in context:
		return word1"""

	#max_index = np.argmax(probs)
	#return model.index2word[max_index]

def minimize_context_dis_word(model, context):
	minimum = 100
	min_word = None
	context_vectors = [model[context_word] for context_word in context]
	context_vec_sum = np.zeros(len(context_vectors[0]))
	for i in range(len(context)):
		context_vec_sum += context_vectors[i]
	for word in model.index2word:
		dis = context_word_distance(model, context, word)
		if dis < minimum and word not in context:
			min_word = word
			minimum = dis
	return min_word

def find_max_dis_word_index(model, context, word_list):
	max_dis = -100
	max_word = None
	max_index = -1
	for i in range(len(word_list)):
		dis = context_word_distance(model, context, word_list[i])
		if dis > max_dis:
			max_dis = dis
			max_word = word_list[i]
			max_index = i
	if max_word != None:
		return max_index
	return None

def minimize_context_dis_word_topn(model, context, n):
	word_list = []
	context_vectors = [model[context_word] for context_word in context]
	context_vec_sum = np.zeros(len(context_vectors[0]))
	for i in range(len(context)):
		context_vec_sum += context_vectors[i]
	for word in model.index2word:
		dis = context_word_distance(model, context, word)
		if len(word_list) < n:
			word_list.append(word)
		else:
			max_dis_index = find_max_dis_word_index(model, context, word_list)
			max_word = word_list[max_dis_index]
			if dis < context_word_distance(model, context, max_word):
				word_list.pop(max_dis_index)
				word_list.append(word)
	return word_list




def main():
	counter = 0
	emendation_scores_dictionary = {}
	emendation_dictionary_unlemm = {}
	lemmatizer = LemmaReplacer('latin')
	j = JVReplacer()
	current_emendation_spot = ""
	#model = Word2Vec.load(sys.argv[2])
	model = Word2Vec.load('last_week_work/latin_library_mc5.model')
	emendations_file = open(sys.argv[1], 'r')
	for line in emendations_file:
		if not ':' in line:
			counter += 1
			current_emendation_spot = line
			emendation_dictionary_unlemm[line] = []
			emendation_scores_dictionary[line] = []
		else:
			line_split = line.split(":")
			identifier = line_split[0]
			line_text = line_split[1]
			line_text = remove_punctuation(line_text)
			lemmatized_line = lemmatizer.lemmatize(line_text)
			final_line = [] 
			for i in range(0, len(lemmatized_line)):
				#lemmatized_line[i] = j.replace(lemmatized_line[i])
				final_line.append(j.replace(lemmatized_line[i]))
			final_line = remove_stopwords(final_line)
			if not all_words_in_model(model, final_line):
				continue
			emendation_scores_dictionary[current_emendation_spot].append((identifier, ' '.join(final_line), 
															model.score([final_line])))
			emendation_dictionary_unlemm[current_emendation_spot].append((identifier, line_text))
	# dictionary is created, now we do the shit for 

	author_emendation_average_ranking = {}

	count = 0
	heyworth_min = 0
	heyworth_max = 0
	for item in sorted(emendation_scores_dictionary.keys()):
		emend_list = []
		scholars = []
		for emend in emendation_scores_dictionary[item]:
			emend_list.append(emend[1].split(' '))
			scholars.append(emend[0])
		if len(emend_list) < 2:
			continue
		differences = detect_difference(emend_list)
		if len(differences) == 0:
			continue
		if len(differences) > len(emend_list):
			continue
		print(item)
		context = find_context_words(emend_list[0], emend_list[1])
		curr_min = 1000000
		curr_max = -1000
		scholar = ""
		worst_scholar = ""
		"""prediction1 = model_prediction(model, context)
		prediction2 = minimize_context_dis_word(model, context)
		print(context)
		print("model prediction is " + prediction1)
		print(context_word_distance(model, context, prediction1))
		print("word in vocabulary that minimizes distance is: " + prediction2)
		print(context_word_distance(model, context, prediction2))
		top_word_list = minimize_context_dis_word_topn(model, context, len(context) + 1)
		result = ""
		for word in top_word_list:
			result += (word + " " + str(context_word_distance(model, context, word)) + " | ") 
		print(result)"""
		for i in range(len(differences)):
			diff = differences[i]
			index = -100
			for j in range(len(emend_list)):
				if diff in emend_list[j]:
					index = j
			#print(scholars[index] + " " + str(emend_list[index]))
			unlemm_line = (emendation_dictionary_unlemm[item])[index][1]

			#print(scholars[index] + " " + str([word for word in emend_list[index] if word != diff]) + " " + diff)
			dis = context_word_distance(model, context, diff)
			#print("cosine distance: " + str(dis))
			print(scholars[index] + ": " + unlemm_line + " | Dis = " + str(dis))
			if dis < curr_min:
				curr_min = dis
				scholar = scholars[index]
			if dis > curr_max:
				curr_max = dis
				worst_scholar = scholars[index]
		if scholar == "Heyworth":
			heyworth_min += 1
		if worst_scholar == "Heyworth":
			heyworth_max += 1
		print("")

		count += 1

	print(str(heyworth_min) + " was number of times Heyworth was deemed best")
	print(str(heyworth_max) + " was number of times Heyworth was deemed worst")
	print(str(count) + " was the total number of examples")
if __name__ == "__main__":
	main()



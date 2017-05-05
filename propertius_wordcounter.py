from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer;
from cltk.stop.latin.stops import STOPS_LIST

import matplotlib.pyplot as plt;
import numpy as np;


import operator;
import sys

stops_extra = ['ego', 'mei', 'mihi', 'me', 'tu', 'tui', 'tibi', 'te', 'meus', 'meo', 'meum', 'mi', 'tuus', 'tui', 'tuo', 'tuum', 'noster'];
stops_augmented = STOPS_LIST;
for word in stops_extra:
	stops_augmented.append(word);

def remove_punctuation(line):
	if "!" in line or "." in line or ";" in line or ":" in line or "," in line:
		return line[:-1];
	return line;

def main():
	jv = JVReplacer();
	more = 0
	lemmatizer = LemmaReplacer('latin');
	word_counts = {};
	lines = open(sys.argv[1]);
	for line in lines:
		words = line.split();
		for i in range(0, len(words)):
			words[i] = jv.replace(remove_punctuation(words[i]).lower());
		for word in words:
			#if word in stops_augmented:
			#	continue;
			if "&" in word:
				continue
			if (len(lemmatizer.lemmatize(word)) == 0):
				more += 1
				continue;

			stem = lemmatizer.lemmatize(word)[0];
			if not stem in word_counts:
				word_counts[stem] = 1;
			else:
				word_counts[stem] = word_counts[stem] + 1;
	words_to_show = 400
	sorted_words = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True);
	top_words = [word[0] for word in sorted_words][0:words_to_show];
	word_freqs = [word[1] for word in sorted_words][0:words_to_show];

	for i in range(0, words_to_show):
		print(str(i) + " " + top_words[i] + " " + str(word_freqs[i]));
	count = 0;
	for i in range(0, words_to_show):
		count += word_freqs[i];
	print(str(count));
	print(str(more))


	s = np.arange(0.0, words_to_show, 1);
	t = word_freqs;
	plt.plot(s, t);
	plt.ylabel('# appearances in Elegiae');
	plt.xlabel('rank of word frequency');
	plt.show();
	

main();




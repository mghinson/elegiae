from ngram_vecs import *
from math import log

def main():
	text_file = open("TextFiles/Book1", 'r')
	text_file2 = open("TextFiles/Book2", 'r')
	text_file3 = open("TextFiles/Book3", 'r')
	text_file4 = open("TextFiles/Book4", 'r')
	four_test = text_file.read() + text_file2.read() + text_file3.read()
	three_test = text_file.read() + text_file2.read() + text_file4.read()
	text_file.close()
	text_file2.close()
	text_file3.close()
	text_file4.close()
	four_test = four_test.replace(" ","").replace("\n'", "")
	three_test = three_test.replace(" ","").replace("\n'", "")

	num_emendations = 4
	emendation1 = "o uigil, iniustae praemia sortis habes"
	emendation1 = emendation1.replace(" ", "")
	emendation2 = "o uigil, iniustae praemia laudis habes"
	emendation2 = emendation2.replace(" ", "")
	emendation3 = "o uigil, iniustae praemia sordis habes"
	emendation3 = emendation3.replace(" ", "")
	emendation4 = "o uigil, iniustae praemia fontis habes"
	emendation4 = emendation4.replace(" ", "")

	ngram_nrange = range(2, 7)
	editors = ["Heyworth", "Peerlkamp", "Baehrens", "Ribbeck"]
	plot_styles = ['r--', 'b--', 'g--', 'k--']
	ng_scores = []
	for i in range(num_emendations):
		ng_scores.append([])
	for i in range(1, 6):
		emend1 = create_ngram_vector(i + 1, emendation1)
		emend2 = create_ngram_vector(i + 1, emendation2)
		emend3 = create_ngram_vector(i + 1, emendation3)
		emend4 = create_ngram_vector(i + 1, emendation4)
		text_string_ngram = create_ngram_vector(i + 1, four_test)
		ng_scores[0].append(cosine_distance(emend1, text_string_ngram))
		ng_scores[1].append(cosine_distance(emend2, text_string_ngram))
		ng_scores[2].append(cosine_distance(emend3, text_string_ngram))
		ng_scores[3].append(cosine_distance(emend4, text_string_ngram))
		print(cosine_distance(emend1, text_string_ngram))
		print(cosine_distance(emend2, text_string_ngram))
		print(cosine_distance(emend3, text_string_ngram))
		print(cosine_distance(emend4, text_string_ngram))
		print("")
	fig = plt.figure(figsize=(30,10))
	gs = gridspec.GridSpec(2, 3, wspace=0.3, hspace=0.3)
	ax = fig.add_subplot(gs[0,0])
	for i in range(num_emendations):
		ax.plot(ngram_nrange, ng_scores[i], plot_styles[i], label=(editors[i] + "'s emendation"))
		ax.set_ylabel("cos distance from Books 1,2,3")
		ax.set_xlabel("n")
	plt.xticks(ngram_nrange)
	ax.grid()
	ax.legend(loc=4)
	plt.show()
if __name__ == "__main__":
	main()

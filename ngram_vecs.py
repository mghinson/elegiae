import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def create_ngram_vector(n, text):
	ngram_dict = {}
	for i in range(len(text) - n):
		ngram = text[i:i + n]
		if not ngram in ngram_dict:
			ngram_dict[ngram] = 1
		else:
			ngram_dict[ngram] = ngram_dict[ngram] + 1
	return ngram_dict

def norm(ngram_vect):
	square_sum = 0
	for key in ngram_vect:
		square_sum += ngram_vect[key] ** 2
	return square_sum ** .5

def dot(vect1, vect2):
	dot = 0
	for key in vect1:
		if key in vect2:
			dot += (vect1[key] * vect2[key])
	return dot

def cosine_distance(vect1, vect2):
	return 1 - dot(vect1, vect2)/(norm(vect1) * norm(vect2))

def main():
	text_file = open("TextFiles/Book1", 'r')
	text_file2 = open("TextFiles/Book2", 'r')
	text_file4 = open("TextFiles/Book3", 'r')
	file_string = text_file.read() + text_file2.read() + text_file4.read()
	text_file.close()
	text_file2.close()
	text_file4.close()
	file_string = file_string.replace(" ","").replace("\n'", "")
	numbers = "0123456789"
	file_string = ''.join([c for c in file_string if not c in numbers])
	num_emendations = 3
	emendation1 = "o vigil iniustae praemia sortis habes"
	emendation1 = emendation1.replace(" ", "")
	emendation2 = "o vigil iniustae praemia laudis habes"
	emendation2 = emendation2.replace(" ", "")
	emendation3 = "o vigil iniustae praemia fontis habes"
	emendation3 = emendation3.replace(" ", "")

	ngram_nrange = [2, 3, 4, 5, 6]
	ng_scores = []
	for i in range(num_emendations):
		ng_scores.append([])
	for i in range(0, 5):
		emend1 = create_ngram_vector(i + 2, emendation1)
		emend2 = create_ngram_vector(i + 2, emendation2)
		emend3 = create_ngram_vector(i + 2, emendation3)
		text_string_ngram = create_ngram_vector(i + 2, file_string)
		ng_scores[0].append(cosine_distance(emend1, text_string_ngram))
		ng_scores[1].append(cosine_distance(emend2, text_string_ngram))
		ng_scores[2].append(cosine_distance(emend3, text_string_ngram))
		print(cosine_distance(emend1, text_string_ngram))
		print(cosine_distance(emend2, text_string_ngram))
		print(cosine_distance(emend3, text_string_ngram))

	fig = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(2, 3, wspace=0.3, hspace=0.3)
	ax = fig.add_subplot(gs[0,0])
	for i in range(num_emendations):
		ax.plot(ngram_nrange, ng_scores[i], label=("emendation " + str(i + 1)))
		ax.set_ylabel("cosine distance")
		ax.set_xlabel("n")
	ax.grid()
	ax.legend()
	plt.show()

if __name__ == "__main__":
	main()



#141019@1102
# A program to find upto n-grams(here 3 grams) of each line from a text file.
import re
import nltk
d = {}
with open ("Data_for_n_grams_of_each_line_of_a_text.txt", "r") as fileHandler: 
    for line in fileHandler: # Here, for loop does not increase complexity, because the whole loop cycle execute only a single time to read each line of the text file.
	    s = line.lower()
	    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
	    tokens = nltk.word_tokenize(s)
		
	    for i in range(len(tokens)):

		    if tokens[i] in d:
			    d[tokens[i]] += 1
		    else:
			    d[tokens[i]] = 1

		    if i < len(tokens) - 1:
			    two_gram = tokens[i] + ' ' + tokens[i + 1]
			    if two_gram in d:
				    d[two_gram] += 1
			    else:
				    d[two_gram] = 1

		    if i < len(tokens) - 2:
			    three_gram = tokens[i] + ' ' + tokens[i + 1] + ' ' + tokens[i + 2]
			    if three_gram in d:
				    d[three_gram] += 1
			    else:
				    d[three_gram] = 1

for key, value in d.items():
	print(key, value)
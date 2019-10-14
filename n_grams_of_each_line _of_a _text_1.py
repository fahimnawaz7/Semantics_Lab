#141019@1100
# A program to find upto n-grams(here 3 grams) of each line from a text file.
import re
import nltk
f = open('n_gram.txt')
# for line in listOfLines:
#     print(line.strip()) 
s = f.read()
# s = "This is my city."
s = s.lower()
s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
tokens = nltk.word_tokenize(s)

d = {}
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
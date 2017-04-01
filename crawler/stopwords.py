f = open('stopwords.txt', 'r')
words = set([word.strip() for word in f.readlines()])

def is_stopword(word):
	return word in words
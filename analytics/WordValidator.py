import nltk

class WordValidator:
	def __init__(self):
		f = open('analytics/stopwords.txt', 'r')
		self.stopwords = set([word.strip() for word in f.readlines()])
		self.english = set(w.lower() for w in nltk.corpus.words.words())

	def is_stopword(self, word):
		return word in self.stopwords

	def is_english(self, word):
		return word in self.english
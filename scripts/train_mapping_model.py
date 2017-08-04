import sys
from nltk import word_tokenize
from collections import Counter

f = open('./love_doc_group.txt','r')
words = word_tokenize(f.read().lower())
love_wordcount = Counter(words)
word_set = list(set(words))
print(word_set)
print(love_wordcount)

import sys, csv, re, json
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
from random import randint
import unidecode

stop_words = list(set(stopwords.words("english")))
more_words = [",","..","'s","'ll","'re","n't","(",")"]
stop_words = stop_words + more_words
doc_group = {}

def load_doc_group(category):
	doc_group[category] = {}
	doc_group[category]['num_docs'] = 0
	lyric_acc= ""
	fails=0
	
	with open('./top_' + category + '_songs.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			artist = re.sub('[^A-Za-z0-9]+', "", row['artist_name']).lower()
			if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
				artist = artist[3:]
			song = re.sub('[^A-Za-z0-9]+', "", row['song_title']).lower()
			lyric_file = artist + "_" + song
			try:
				f = open('./lyrics_depo/' + lyric_file + '.txt','r')
				lyric_acc= lyric_acc + '\n\n' + unidecode.unidecode(f.read().lower())
				f.close()
				doc_group[category]['num_docs'] += 1
			except Exception as e:
				if e.errno != 2:
					print("Exception occured: " + str(e))
				fails += 1
	
	doc_group[category]['frequencies'] = Counter([x for x in word_tokenize(lyric_acc) if x not in stop_words])
	print("Could not find " + str(fails) + " songs in lyrics_depo for category '" + category + "'.")

def load_baseline_doc_group():
	doc_group['baseline'] = {}
	doc_group['baseline']['num_docs'] = 0
	lyric_acc= ""
	fails=0
	
	with open('./distinct_top_40_songs.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if doc_group['baseline']['num_docs'] == 79:
				break
			if randint(0,50) > 49:
				artist = re.sub('[^A-Za-z0-9]+', "", row['artist_name']).lower()
				if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
					artist = artist[3:]
				song = re.sub('[^A-Za-z0-9]+', "", row['song_title']).lower()
				lyric_file = artist + "_" + song
				try:
					f = open('./lyrics_depo/' + lyric_file + '.txt','r')
					lyric_acc= lyric_acc + '\n\n' + unidecode.unidecode(f.read().lower())
					f.close()
					doc_group['baseline']['num_docs'] += 1
				except Exception as e:
					if e.errno != 2:
						print("Exception occured: " + str(e))
					fails += 1
	doc_group['baseline']['frequencies'] = Counter([x for x in word_tokenize(lyric_acc) if x not in stop_words])
	print("Could not find " + str(fails) + " songs in lyrics_depo for category 'baseline'.")
		
load_doc_group('love')
load_baseline_doc_group()

f = open('./frequency_scores.csv','w+')
f.write("term,love_freq,base_freq\n")

for term in doc_group['love']['frequencies']:
	try:
		love_freq = str(doc_group['love']['frequencies'][term])
		base_freq = str(doc_group['baseline']['frequencies'][term])
		f.write(term + "," + love_freq + "," + base_freq + "\n")
	except Exception as e:
		pass

f.close()

#with open('./document_groups.json', 'w+') as jf:
    #json.dump(doc_group, jf)
			
	
	
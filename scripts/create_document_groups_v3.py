import sys, csv, re, json
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
from random import randint
import unidecode

stop_words = list(set(stopwords.words("english")))
stop_words = stop_words.append([",","..","'s","'ll","'re","n't","(",")","."])
cat_songs = {}
base_songs = {}

def process_lyrics(str):
	unwanted_chars = ['\"','\'',',',';',':','-','~','?','!','.','(',')','[',']','{','}','/']
	str = unidecode.unidecode(str.lower())
	for char in unwanted_chars:
		str = str.replace(char,'')
	return list(set(str.split()))

def load_doc_group(category):
	fails=0
	with open('../new_' + category + '_songs.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			artist = re.sub('[^A-Za-z0-9]+', "", row['artist_name']).lower()
			if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
				artist = artist[3:]
			song = re.sub('[^A-Za-z0-9]+', "", row['song_title']).lower()
			lyric_file = artist + "_" + song
			try:
				f = open('../lyrics_depo/' + lyric_file + '.txt','r')
				term_set= process_lyrics(f.read())
				f.close()
				cat_songs[lyric_file] = (list(term_set),category)
			except Exception as e:
				if e.errno != 2:
					print("Exception occured: " + str(e))
				fails += 1
	
	print("Could not find " + str(fails) + " songs in lyrics_depo for category '" + category + "'.")

def load_base_doc_group():
	fails=0
	with open('../output/distinct_top_40_songs.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			#if doc_group['baseline']['num_docs'] == 10000:
				#break
			if randint(0,50) > -1:
				artist = re.sub('[^A-Za-z0-9]+', "", row['artist_name']).lower()
				if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
					artist = artist[3:]
				song = re.sub('[^A-Za-z0-9]+', "", row['song_title']).lower()
				lyric_file = artist + "_" + song
				try:
					f = open('../lyrics_depo/' + lyric_file + '.txt','r')
					term_set= process_lyrics(f.read())
					f.close()
					base_songs[lyric_file] = list(term_set)
				except Exception as e:
					#if e.errno != 2:
					#print("Exception occured: " + str(e))
					fails += 1
	print("Could not find " + str(fails) + " songs in lyrics_depo for category 'baseline'.")
		
load_doc_group('love')
load_base_doc_group()

class Counter(dict):
	def __missing__(self,key):
		return 0
		
love_term_freqs = Counter()
base_term_freqs = Counter()
base_song_count = 0
love_song_count = 0

for song in base_songs:
	for term in base_songs[song]:
		base_term_freqs[term] = 1 + base_term_freqs[term]
	base_song_count+=1
		
for song in cat_songs:
	for term in cat_songs[song][0]:
		love_term_freqs[term] = 1 + love_term_freqs[term]
	love_song_count+=1

top_love_terms = []

for term in love_term_freqs:
	love_freq = love_term_freqs[term]
	norm_love_freq = float(love_term_freqs[term]/love_song_count)
	norm_base_freq = float(base_term_freqs[term]/base_song_count)
	if norm_base_freq > 0:
		love_ratio = norm_love_freq/norm_base_freq
		if love_freq > 7 and love_ratio > 2:
			top_love_terms.append((love_ratio,term))
			
top_love_terms.sort(reverse=True)

f = open('../output/love_term_weights.csv','w+')
f.write("term,score\n")
for term in top_love_terms:
	f.write(term[1] + "," + str(term[0])+"\n")
f.close()

#with open('../output/document_groups.json', 'w+') as jf:
    #json.dump(songs, jf)
			
	
	
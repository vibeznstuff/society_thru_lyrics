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
	with open('../category_training/' + category + '_songs.csv') as csvfile:
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
				#if e.errno != 2:
					#print("Exception occured: " + str(e))
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
load_doc_group('political')
load_doc_group('sad')
load_doc_group('sexual')
load_base_doc_group()

class Counter(dict):
	def __missing__(self,key):
		return 0
		

base_song_count = 0
base_term_freqs = Counter()

political_song_count = 0
political_term_freqs = Counter()
top_political_terms = []

love_song_count = 0
love_term_freqs = Counter()
top_love_terms = []

sad_song_count = 0
sad_term_freqs = Counter()
top_sad_terms = []

sexual_song_count = 0
sexual_term_freqs = Counter()
top_sexual_terms = []



for song in base_songs:
	for term in base_songs[song]:
		base_term_freqs[term] = 1 + base_term_freqs[term]
	base_song_count+=1
		
for song in cat_songs:
	if cat_songs[song][1] == 'love':
		for term in cat_songs[song][0]:
			love_term_freqs[term] = 1 + love_term_freqs[term]
		love_song_count+=1
	
for song in cat_songs:
	if cat_songs[song][1] == 'political':
		for term in cat_songs[song][0]:
			political_term_freqs[term] = 1 + political_term_freqs[term]
		political_song_count+=1

for song in cat_songs:
	if cat_songs[song][1] == 'sad':
		for term in cat_songs[song][0]:
			sad_term_freqs[term] = 1 + sad_term_freqs[term]
		sad_song_count+=1

for song in cat_songs:
	if cat_songs[song][1] == 'sexual':
		for term in cat_songs[song][0]:
			sexual_term_freqs[term] = 1 + sexual_term_freqs[term]
		sexual_song_count+=1

for term in love_term_freqs:
	love_freq = love_term_freqs[term]
	norm_love_freq = float(love_term_freqs[term]/love_song_count)
	norm_base_freq = float(base_term_freqs[term]/base_song_count)
	if norm_base_freq > 0:
		love_ratio = (norm_love_freq/norm_base_freq)
		if love_freq > love_song_count*0.05 and love_ratio > 2:
			top_love_terms.append((love_ratio,term))
			
for term in political_term_freqs:
	political_freq = political_term_freqs[term]
	norm_political_freq = float(political_term_freqs[term]/political_song_count)
	norm_base_freq = float(base_term_freqs[term]/base_song_count)
	if norm_base_freq > 0:
		political_ratio = (norm_political_freq/norm_base_freq)
		if political_freq > political_song_count*0.05 and political_ratio > 2:
			top_political_terms.append((political_ratio,term))
			
for term in sad_term_freqs:
	sad_freq = sad_term_freqs[term]
	norm_sad_freq = float(sad_term_freqs[term]/sad_song_count)
	norm_base_freq = float(base_term_freqs[term]/base_song_count)
	if norm_base_freq > 0:
		sad_ratio = (norm_sad_freq/norm_base_freq)
		if sad_freq > sad_song_count*0.05 and sad_ratio > 2:
			top_sad_terms.append((sad_ratio,term))

for term in sexual_term_freqs:
	sexual_freq = sexual_term_freqs[term]
	norm_sexual_freq = float(sexual_term_freqs[term]/sexual_song_count)
	norm_base_freq = float(base_term_freqs[term]/base_song_count)
	if norm_base_freq > 0:
		sexual_ratio = (norm_sexual_freq/norm_base_freq)
		if sexual_freq > sexual_song_count*0.05 and sexual_ratio > 2:
			top_sexual_terms.append((sexual_ratio,term))
			
top_love_terms.sort(reverse=True)
top_political_terms.sort(reverse=True)
top_sad_terms.sort(reverse=True)
top_sexual_terms.sort(reverse=True)

print("Total Love Songs: " + str(love_song_count))
print("Total Political Songs: " + str(political_song_count))
print("Total Sad Songs: " + str(sad_song_count))
print("Total Sexual Songs: " + str(sexual_song_count))
print("Total Base Songs: " + str(base_song_count))

f = open('../output/love_term_weights.csv','w+')
f.write("term,score\n")
for term in top_love_terms:
	f.write(term[1] + "," + str(term[0])+"\n")
f.close()

f = open('../output/political_term_weights.csv','w+')
f.write("term,score\n")
for term in top_political_terms:
	f.write(term[1] + "," + str(term[0])+"\n")
f.close()

f = open('../output/sad_term_weights.csv','w+')
f.write("term,score\n")
for term in top_sad_terms:
	f.write(term[1] + "," + str(term[0])+"\n")
f.close()

f = open('../output/sexual_term_weights.csv','w+')
f.write("term,score\n")
for term in top_sexual_terms:
	f.write(term[1] + "," + str(term[0])+"\n")
f.close()

#with open('../output/document_groups.json', 'w+') as jf:
    #json.dump(songs, jf)
			
	
	
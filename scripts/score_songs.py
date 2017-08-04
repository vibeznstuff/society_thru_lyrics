import csv, re, nltk, math, re
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

stemmer = SnowballStemmer("english")

def load_lyrics(artist,song):
	song_file = open(".\\lyrics_depo\\"+artist+"_"+song+".txt","r")
	song = song_file.read().lower()
	lyric_contents =  re.sub(r"[\n]+"," ",song)
	return lyric_contents

def get_category_score(category,lyric_contents,scores):
	with open(".\\category_maps2\\" + category + ".csv") as csvfile:
		reader = csv.DictReader(csvfile)
		score=0
		breadth=0
		for row in reader:
			hits = re.findall(" " + row['reg_exp'].lower(),lyric_contents)
			num_hits = len(hits)
			#if num_hits > 0:
				#print("Category :" + category)
				#print(row['reg_exp'])
				#print(hits)
			score+=num_hits
			if num_hits > 0:
				breadth+=1
		if breadth == 0:
			scores[category]='0'
		else:
			scores[category]=str(math.ceil(score*math.log(breadth+1)))

def process_song(artist,song):
	scores = {}
	lyric_contents = load_lyrics(artist,song)
	get_category_score("romance",lyric_contents,scores)
	get_category_score("dark",lyric_contents,scores)
	get_category_score("political",lyric_contents,scores)
	get_category_score("sexuality",lyric_contents,scores)
	get_category_score("vulgar",lyric_contents,scores)
	get_category_score("drugs",lyric_contents,scores)
	get_category_score("violence",lyric_contents,scores)
	return scores

f = open(".\\scored_songs_v2.csv","w+")
f.write("year,month,rank,artist,song,romance_score,dark_score,political_score,sexuality_score,vulgar_score,drugs_score,violence_score\n")

with open(".\\historic_top_40_songs_1960_2017.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		counter = 0
		for row in reader:
			year = row['year']
			month = row['month']
			rank = row['rank']
			artist = row['artist_name'].lower()
			song = row['song_title'].lower()
			
			artist = re.sub('[^A-Za-z0-9]+', "", artist)
			song = re.sub('[^A-Za-z0-9]+', "", song)
			if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
				artist = artist[3:]
			counter += 1
			try: 
				#print("Artist: " + artist + ", Song: " + song)
				scores=process_song(artist,song)
				#print(scores)
				f.write(year+","+month+","+rank+","+artist+","+song+","+scores['romance']+","+scores['dark']+ \
				","+scores['political']+","+scores['sexuality']+","+scores['vulgar']+ \
				","+scores['drugs']+","+scores['violence']+"\n")
			except Exception as e:
				#print(e)
				pass

f.close()
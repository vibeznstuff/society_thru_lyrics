import csv, re, nltk, math, re
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

stemmer = SnowballStemmer("english")

def load_lyrics(artist,song):
	song_file = open("../lyrics_depo/"+artist+"_"+song+".txt","r")
	song = song_file.read().lower()
	lyric_contents =  re.sub(r"[\n]+"," ",song)
	return lyric_contents

def get_love_score(lyric_contents,scores):
	with open("../output/love_term_weights.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		total_score=0.0
		for row in reader:
			hit_flag = min(max(lyric_contents.find(row['term']),0),1)
			hit_score = hit_flag * (float(row['score'])-1)
			#hits = re.findall(" " + row['reg_exp'].lower(),lyric_contents)
			#num_hits = len(hits)
			#if num_hits > 0:
				#print("Category :" + category)
				#print(row['reg_exp'])
				#print(hits)
			total_score+=hit_score
		scores['love']=str(math.ceil(total_score))
		
def get_political_score(lyric_contents,scores):
	with open("../output/political_term_weights.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		total_score=0.0
		for row in reader:
			hit_flag = min(max(lyric_contents.find(row['term']),0),1)
			hit_score = hit_flag * (float(row['score'])-1)
			#hits = re.findall(" " + row['reg_exp'].lower(),lyric_contents)
			#num_hits = len(hits)
			#if num_hits > 0:
				#print("Category :" + category)
				#print(row['reg_exp'])
				#print(hits)
			total_score+=hit_score
		scores['political']=str(math.ceil(total_score))
		
def get_sad_score(lyric_contents,scores):
	with open("../output/sad_term_weights.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		total_score=0.0
		for row in reader:
			hit_flag = min(max(lyric_contents.find(row['term']),0),1)
			hit_score = hit_flag * (float(row['score'])-1)
			#hits = re.findall(" " + row['reg_exp'].lower(),lyric_contents)
			#num_hits = len(hits)
			#if num_hits > 0:
				#print("Category :" + category)
				#print(row['reg_exp'])
				#print(hits)
			total_score+=hit_score
		scores['sad']=str(math.ceil(total_score))

def get_sexual_score(lyric_contents,scores):
	with open("../output/sexual_term_weights.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		total_score=0.0
		for row in reader:
			hit_flag = min(max(lyric_contents.find(row['term']),0),1)
			hit_score = hit_flag * (float(row['score'])-1)
			#hits = re.findall(" " + row['reg_exp'].lower(),lyric_contents)
			#num_hits = len(hits)
			#if num_hits > 0:
				#print("Category :" + category)
				#print(row['reg_exp'])
				#print(hits)
			total_score+=hit_score
		scores['sexual']=str(math.ceil(total_score))

def process_song(artist,song):
	scores = {}
	lyric_contents = load_lyrics(artist,song)
	get_love_score(lyric_contents,scores)
	#get_category_score("romance",lyric_contents,scores)
	get_sad_score(lyric_contents,scores)
	get_political_score(lyric_contents,scores)
	get_sexual_score(lyric_contents,scores)
	#get_category_score("vulgar",lyric_contents,scores)
	#get_category_score("drugs",lyric_contents,scores)
	#get_category_score("violence",lyric_contents,scores)
	return scores

f = open("../output/scored_songs.csv","w+")
#f.write("year,month,rank,artist,song,romance_score,dark_score,political_score,sexuality_score,vulgar_score,drugs_score,violence_score\n")
f.write("year,month,rank,artist,song,romance_score,political_score,sad_score,sexual_score\n")

with open("../output/historic_top_40_songs_1960_2017.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			year = str(row['year'])
			month = str(row['month'])
			rank = str(row['rank'])
			artist = row['artist_name'].lower()
			song = row['song_title'].lower()
			
			artist = re.sub('[^A-Za-z0-9]+', "", artist)
			song = re.sub('[^A-Za-z0-9]+', "", song)
			if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
				artist = artist[3:]
			try: 
				#print("Artist: " + artist + ", Song: " + song)
				scores=process_song(artist,song)
				#print(scores)
				f.write(year+","+month+","+rank+","+artist+","+song+","+scores['love']+","+scores['political']+","+scores['sad']+","+scores['sexual']+"\n")
			except FileNotFoundError as e:
				pass
			except UnicodeDecodeError as u:
				print("Unicode Decode Error with song: " + artist + " // " + song)
				#print(u)
				pass

f.close()
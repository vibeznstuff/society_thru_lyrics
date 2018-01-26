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
		
def get_cat_score(lyric_contents,scores,cat):
	with open("../output/"+cat+"_term_weights.csv") as csvfile:
		reader = csv.DictReader(csvfile)
		total_score=0.0
		for row in reader:
			hit_flag = min(max(lyric_contents.find(row['term']),0),1)
			hit_score = hit_flag * (float(row['score'])-1)
			total_score+=hit_score
		scores[cat]=str(math.ceil(total_score))

def process_song(artist,song):
	scores = {}
	categories = ["love","sad","political","sexual"]
	lyric_contents = load_lyrics(artist,song)
	
	#Loop through categories to score data
	for cat in categories:
		get_cat_score(lyric_contents,scores,cat)
	return scores

f = open("../output/scored_songs.csv","w+")
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
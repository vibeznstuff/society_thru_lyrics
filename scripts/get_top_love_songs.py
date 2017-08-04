import re, sys
import urllib.request
import time
import unidecode
from bs4 import BeautifulSoup

def open_charts_page(url):
    try:
        content = urllib.request.urlopen(url).read()
        return content
    except urllib.error.HTTPError as err:
        if err.code == 503:
            print("Reached a 503 error...re-trying")
            time.sleep(20)
            content = urllib.request.urlopen(url).read()
            return content
        else:
            raise

track_set = []

def get_song_list_1():
	content = open_charts_page('https://www.thoughtco.com/top-best-love-songs-of-all-time-3248359')
	soup = BeautifulSoup(content,'html.parser')
	top_list = soup.find_all('h3',{'class': 'heading heading-inline'})
	#Loop over this...
	#rank=0 #Top 40 tracker
	for track in top_list:
		artist = unidecode.unidecode(track.text.split(" - ")[0]).strip()
		song = unidecode.unidecode(track.text.split(" - ")[1])[1:len(unidecode.unidecode(track.text.split(" - ")[1]))].split("\"")[0].strip()
		artist = artist.split("feat")[0]
		if artist.lower().strip() == 'beyonce':
			artist = 'Beyonce Knowles'
		song = song.replace(",","")
		print(song + " by " + artist)
		track_set.append((artist,song))

def get_song_list_2():
	content = open_charts_page('http://www.billboard.com/articles/list/6792625/top-50-love-songs-of-all-time')
	soup = BeautifulSoup(content,'html.parser')
	top_list = soup.find_all('h3',{'class': 'list-data__title'})
	#Loop over this...
	#rank=0 #Top 40 tracker
	for track in top_list:
		songbyartist = unidecode.unidecode(track.text.split("\n")[0][1:len(track.text.split("\n")[0])])
		song = songbyartist.split("\"")[0].replace(",","").strip()
		artist = songbyartist.split("\"")[1].replace("-","").strip()
		artist = artist.split("feat")[0]
		print(song + " by " + artist)
		track_set.append((artist,song))
		

get_song_list_1()
get_song_list_2()

track_set = set(track_set)

f = open('./top_love_songs.csv','w+')
f.write("artist_name,song_title\n")
for track in track_set:
	f.write(track[0] + ',' + track[1])
	f.write('\n')
f.close()	

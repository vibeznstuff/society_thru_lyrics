import re, sys, csv, time, random
from fake_useragent import UserAgent
import urllib.request, os.path
from bs4 import BeautifulSoup
 
#ua = UserAgent()
User_Agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0']

def get_lyrics(artist,song_title):
	artist = artist.lower()
	song_title = song_title.lower()
	# remove all except alphanumeric characters from artist and song_title
	artist = re.sub('[^A-Za-z0-9]+', "", artist)
	song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
	if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
		artist = artist[3:]
	print("Artist: " + artist + ", Song: " + song_title)
	url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
	req = urllib.request.Request(
		url, 
		data=None, 
		headers={
	'User-Agent': User_Agents[random.randint(1,4)]
		}
	)
	try:
		content = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(content, 'html.parser')
		lyrics = str(soup)
		# lyrics lies between up_partition and down_partition
		up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
		down_partition = '<!-- MxM banner -->'
		lyrics = lyrics.split(up_partition)[1]
		lyrics = lyrics.split(down_partition)[0]
		lyrics = lyrics.replace('<br>','').replace('</br>','').replace('<br/>','').replace('</div>','').replace('<i>','').replace('</i>','').strip()
		lyrics = re.sub(r'\[.*\]',"",lyrics)
		file = open("../lyrics_depo/"+artist+"_"+song_title+".txt","w+")
		file.write(lyrics)
		file.close()
		return artist + " - " + song_title + " was added to lyrics depo."
	except Exception as e:
		return "Exception occurred \n" +str(e)

def extract_lyrics(song_list_path):
	with open(song_list_path) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				artist = row['artist_name'].lower()
				song_title = row['song_title'].lower()
				# remove all except alphanumeric characters from artist and song_title
				artist = re.sub('[^A-Za-z0-9]+', "", artist)
				song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
				if os.path.exists('../lyrics_depo/'+artist+'_'+song_title+'.txt') == False:
					time.sleep(random.randint(10,25))
					print(get_lyrics(row['artist_name'],row['song_title']))
			except Exception as e:
				pass

def main(argv):
	extract_lyrics('../category_training/new_love_songs.csv')

if __name__ == "__main__":
	main(sys.argv[1:])

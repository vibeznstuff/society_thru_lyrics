import os

path = "../lyrics_depo/"

f = open('../output/lyric_depo_song_list.csv','w+')
f.write("artist_name,song_title\n")

for file in os.listdir(path):
	#print(file.split("_"))
	artist,song=file.split("_")
	f.write(artist+","+song.split(".")[0]+"\n")
	
f.close()
	
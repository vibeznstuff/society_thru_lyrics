import re, sys
import urllib.request
import time
import sys
import unidecode
from bs4 import BeautifulSoup

def open_charts_page(date):
    try:
        content = urllib.request.urlopen('http://www.officialcharts.com/charts/singles-chart/' + date + '/7501/').read()
        return content
    except urllib.error.HTTPError as err:
        if err.code == 503:
            print("Reached a 503 error...re-trying")
            time.sleep(20)
            content = urllib.request.urlopen('http://www.officialcharts.com/charts/singles-chart/' + date + '/7501/').read()
            return content
        else:
            raise

def get_song_list():
	f = open('./historic_top_40s_1960_2017.csv','a+')
	years = ['1960', '1961','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017']
	months = ['01','02','03','04','05','06','07','08','09','10','11','12']
	for year in years:
		if int(year) >= 1991:
			for month in months:
				time.sleep(3)
				date = year + month + '01'
				content = open_charts_page(date)
				soup = BeautifulSoup(content,'html.parser')
				top_list = soup.find_all('div',{'class': 'title-artist'})
				#Loop over this...
				rank=0 #Top 40 tracker
				print(date)
				for track in top_list:
					rank+=1
					song = unidecode.unidecode(track.find('div',{'class':'title'}).find("a").text)
					artist = unidecode.unidecode(track.find('div',{'class':'artist'}).find("a").text)
					artist = artist.split("/")[0].split("FT")[0]
					f.write(year + ',' + month + ',' + str(rank) + ',' + song + ',' + artist)
					f.write('\n')
	f.close()
		
get_song_list()
	

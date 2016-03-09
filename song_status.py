import sys, os
import urllib2
song_name = ""
if(len(sys.argv) == 2):
	song_name = sys.argv[1]
else:
	song_name = raw_input("Enter the song: ")
import requests,time,re,zipfile
from bs4 import BeautifulSoup

url = "http://subscene.com/subtitles/title?q=" + song_name
r = requests.get(url)
soup=BeautifulSoup(r.content)
song_list = []
i = 0
for row in soup.find_all('div', {"class" : "title"}):
	s = row.find('a')
	i = i + 1
	print(str(i) + ".) " + s.contents[0])
	song_list.append("http://subscene.com/" + s["href"] + "/english")
choice = int(raw_input("Enter the choice: "))

song_full_name = soup.find_all('div', {"class" : "title"})[choice-1].find('a').contents[0]
url = song_list[choice-1]
r = requests.get(url)
soup=BeautifulSoup(r.content)
row = soup.find('td', {"class" : "a1"})
gist = row.find('a')

url = "http://subscene.com" + gist["href"]
r = requests.get(url)
soup=BeautifulSoup(r.content)
button = soup.find('a', {"id" : "downloadButton"})

url = "http://subscene.com" + button["href"]
r = requests.get(url)
soup=BeautifulSoup(r.content,"lxml")
time.sleep(1)
song_save = "temp_" + song_name
if os.path.exists(song_save):
	import shutil
	shutil.rmtree(song_save)
subfile=open(song_save + ".zip", 'wb')
for chunk in r.iter_content(100000):
	subfile.write(chunk)
	subfile.close()
 	time.sleep(1)
 	zip=zipfile.ZipFile(song_save +".zip")
 	zip.extractall(song_save)
 	zip.close()
 	os.unlink(song_save + ".zip")

path = song_save
song_srt = song_save + "/" + os.listdir(path)[0]
total_time = 0
start_time = None
end_time = None

if song_srt[-3:]=="srt":
	import pysrt
	s = pysrt.open(song_srt,encoding="iso-8859-1")
	start_phrase = raw_input("Enter starting phrase ")
	end_phrase = raw_input("Enter ending phrase ")
	start_time = None
	end_time = None
	for i in s.data:
		if start_phrase in i.text.lower():
			dummy = i.start
			start_time = dummy.minutes * 60 + dummy.seconds
		if (end_phrase in i.text.lower()) and (start_time is not None):
			dummy = i.start
			end_time = dummy.minutes * 60 + dummy.seconds
			break
	ttl = s.data[len(s)-1].end
	total_time = ttl.minutes * 60 + ttl.seconds

	url = "https://www.youtube.com/results?search_query=" + song_full_name[:-6]
	r = requests.get(url)
	soup=BeautifulSoup(r.content)
	to_url = None
	for row in soup.find_all('a', {"class" : "yt-uix-sessionlink        spf-link "}):
		span_in = row.find('span', {"class" : "video-time"}).contents[0]
		total_time_this = (ord(span_in[0])-ord('0'))*60 + (ord(span_in[2])- ord('0'))*10 + ord(span_in[3])- ord('0')
		if(abs(total_time_this - total_time) < 30):
			to_url = "https://www.youtube.com" + row["href"] + "&start=" + str(start_time) + "&end=" + str(end_time)
			break
	print "Start Time of phrase is: " + str(start_time/60) + ":" + str(start_time%60)
	print "End Time of phrase is: " + str(end_time/60) + ":" + str(end_time%60)
	if to_url is not None:
		print "Post this URL(video): " + to_url
	else:
		print "Sorry But I couldn't fetch you a video link"
else:
	print ("Sorry I couldn't find the srt.")

if os.path.exists(song_save):
	import shutil
	shutil.rmtree(song_save)

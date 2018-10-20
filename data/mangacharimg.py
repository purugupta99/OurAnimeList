import requests
from bs4 import BeautifulSoup
import csv
import base64
import os


with open("./mangachars.csv", "r") as file:
	read = csv.reader(file, delimiter=";")
	i=0
	for row in read:
		print(row[3] , i)
		if row[3] != "Url_Char" and i>276:
			r = requests.get(row[3])
			source = BeautifulSoup(r.content, "lxml")
			content = source.find("div", {"id": "contentWrapper"})
			#try:
			img_url = content.find('img')['src']
			img_data = requests.get(img_url)
			print('\ '.join(row[0].rsplit()))
			os.system("mkdir ../static/images/manga_characters/"+('\ '.join(row[0].rsplit())))
			image_file = open("../static/images/manga_characters/" +row[0]+"/"+row[1]+".jpg", "wb")
			for chunk in img_data.iter_content(10000):
				image_file.write(chunk)
			image_file.close()
			#except:
			#	pass
		i+=1
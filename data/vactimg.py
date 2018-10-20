import requests
from bs4 import BeautifulSoup
import csv
import base64
import os


with open("./character.csv", "r") as file:
	read = csv.reader(file, delimiter=";")
	i=0
	for row in read:
		print(row[4] , i)
		if row[4] != "url_actor" and row[4] != "Not Available" and i>178 :
			r = requests.get(row[4])
			source = BeautifulSoup(r.content, "lxml")
			content = source.find("div", {"id": "contentWrapper"})
			try:
				img_url = content.find('img')['src']
				img_data = requests.get(img_url)
				image_file = open("../static/images/characters/" +row[0]+"/"+row[5]+".jpg", "wb")
				for chunk in img_data.iter_content(10000):
					image_file.write(chunk)
				image_file.close()
			except:
				pass
		i+=1
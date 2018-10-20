import requests
from bs4 import BeautifulSoup
import csv
import base64
import os


with open("./character.csv", "r") as file:
	read = csv.reader(file, delimiter=";")
	i=0
	for row in read:
		print(row[1] , i)
		if row[1] != "url_char" and i > 409:
			r = requests.get(row[1])
			source = BeautifulSoup(r.content, "lxml")
			content = source.find("div", {"id": "contentWrapper"})
			try:
				img_url = content.find('img')['src']
				img_data = requests.get(img_url)
				image_file = open("../static/images/characters/" +row[0]+"/"+row[2]+".jpg", "wb")
				for chunk in img_data.iter_content(10000):
					image_file.write(chunk)
				image_file.close()
			except:
				pass
		i+=1
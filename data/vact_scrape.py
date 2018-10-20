import requests
from bs4 import BeautifulSoup
import csv
import base64
import os

with open("./character.csv","r") as file:
	read=csv.reader(file,delimiter=";")
	for row in read:
		print (row[4])
		if row[4]!="Url_Actor" and row[4]!="Not Available":
			r = requests.get(row[4])
			source = BeautifulSoup(r.content, "lxml")
			content=source.find("div" , {"id" : "contentWrapper"})
			head=content.find("div").find("h1").get_text()
			print(head)
			data=content.find("div" , {"id" : "content"})
			info=data.find("td")
			print()
			pe=info.find_all("span" , { "class" : "dark_text" })
			for p in pe:
				if p.get_text() == "Birthday:":
					print(p.get_text())
					print(p.nextSibling)
			link=info.find_all("a")
			print(link[7]['href'])
			moredata=info.find("div" , { "class" : "people-informantion-more js-people-informantion-more"})
			print(moredata.get_text())
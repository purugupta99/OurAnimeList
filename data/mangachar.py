import requests
from bs4 import BeautifulSoup
import csv
import base64
import os

main_url = "https://myanimelist.net/topmanga.php"
req = requests.get(main_url)
htmltext = BeautifulSoup(req.content, "lxml")

manga_URL = []
manga = htmltext.find_all("a", {"class": "hoverinfo_trigger fs14 fw-b"})
tab_gen = [["Name_Eng", "Genre"]]

for i in manga:
	manga_URL.append(i['href'])

final = [["Name_Manga","Name_Char" , "Role_Char" , "Url_Char"]]

for url in manga_URL:
	r = requests.get(url)
	print(url)
	source = BeautifulSoup(r.content, "lxml")
	content = source.find("div", {"id": "contentWrapper"})
	name_manga=content.find("span" ,  { "itemprop" : "name" } ).get_text()
	try:
		chardet=content.find("div" , { "class" : "detail-characters-list clearfix" } )
		tabs=chardet.find_all("table")
		for tab in tabs:
			td=tab.find_all("td")
			name_char=td[1].find("a").get_text()
			role_char=td[1].find("small").get_text()
			url_char=td[1].find("a")['href']
			final.append([name_manga,name_char,role_char,url_char])
			print(final)
	except:
		pass
print(final)

with open('./mangachars.csv', 'w') as file:
	writer = csv.writer(file, delimiter=";")
	for row in final:
		writer.writerow(row)
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

final = [["Rank", "Popularity", "Score", "Name_eng" ,"Altername_eng", "Synonyms", "Name_Jap", "Cast_Type", "Volumes_Num", "Chapters_Num" ,"Status", "Published", "Genres", "Authors" , "Serialization" ,"Synopsis"]]

for url in manga_URL:
	r = requests.get(url)
	source = BeautifulSoup(r.content, "lxml")
	content = source.find("div", {"id": "contentWrapper"})
	print(url)
	img_url = content.find('img')['src']
	img_data = requests.get(img_url)
	name=content.find("span" ,  { "itemprop" : "name" } ).get_text()
	image_file = open("../static/images/manga/"+name+".jpg", "wb")
	for chunk in img_data.iter_content(10000):
		image_file.write(chunk)
	image_file.close()
	print("img-url" ,img_url)
	'''except:
		print("jello")
		pass'''

	'''try:
		score = (source.find("div", {"class": "fl-l score"}).contents[0].rsplit()[0])
		print(score)
	except:
		pass
	try:
		rank = (source.find("span", {"class": "numbers ranked"}).find("strong").contents[0])
		print(rank)
	except:
		pass
	try:
		popularity = (source.find("span", {"class": "numbers popularity"}).find("strong").contents[0])
		print(popularity)
	except:
		pass
	try:
		synopsis = (source.find("span", {"itemprop": "description"}).get_text())
	except:
		synopsis=""
	name_eng=source.find("span" , { "itemprop" : "name" } ).get_text()
	temp = source.find("div", {"class": "js-scrollfix-bottom"}).find_all("div")
	p=4
	if ' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "English:":
		altername_eng = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(altername_eng)
		p+=1
	else:
		altername_eng=""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Synonyms:"):
		synonym = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(synonym)
		p += 1
	else:
		synonym = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Japanese:"):
		name_jap = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(name_jap)
		p += 1
	else:
		name_jap = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Type:"):
		cast_type = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(cast_type)
		p += 1
	else:
		cast_type = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Volumes:"):
		volumes_num = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(volumes_num)
		p += 1
	else:
		volumes_num = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Chapters:"):
		chapters_num = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(chapters_num)
		p += 1
	else:
		chapters_num = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Status:"):
		status = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(status)
		p += 1
	else:
		status = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Published:"):
		published = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(published)
		p += 1
	else:
		published = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Genres:"):
		genres = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(genres)
		p += 1
	else:
		genres = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Authors:"):
		authors = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(authors)
		p += 1
	else:
		authors = ""
	if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Serialization:"):
		serialization = (' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:]))
		print(serialization)
		p += 1
	else:
		serialization = ""
	print(synopsis)
	charlist=source.find( "div" , { "class" : "detail-characters-list clearfix" } )
	try:
		ans=charlist.find_all("a")
		roles=charlist.find_all("small")
		i=1
		j=0
		while i < len(ans):
			print(ans[i].get_text())
			print(ans[i]["href"])
			print(roles[j].get_text())
			j+=1
			i+=2
	except:
		pass
	for g in (genres.rsplit(',')):
		entry_gen = [name_eng, g.rsplit()[0]]
		print (entry_gen)
		tab_gen.append(entry_gen)
	final.append([rank[1:] , popularity[1:] , score , name_eng ,altername_eng , synonym , name_jap , cast_type , volumes_num , chapters_num ,status , published , genres , authors , serialization ,synopsis])'''


'''
with open('./mangadata.csv', 'w') as file:
	writer = csv.writer(file, delimiter=";")
	for row in final:
		writer.writerow(row)
with open('./genremanga.csv', 'w') as file:
	writer = csv.writer(file, delimiter=";")
	for row in tab_gen:
		writer.writerow(row)
	file.close()

'''
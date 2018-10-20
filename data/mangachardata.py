import requests
from bs4 import BeautifulSoup
import csv
import base64
import os

final=[["Char_Name","Name_Jap","Name_Nick","Char_Data"]]
with open("./mangachars.csv","r") as file:
	read=csv.reader(file,delimiter=";")
	for row in read:
		#print (row[1])
		if row[3]!="Url_Char":
			Animeography=[]
			Mangaography=[]
			char_data=""
			Voice_actors=[]
			char_name=row[1]
			r = requests.get(row[3])
			source = BeautifulSoup(r.content, "lxml")
			content=source.find("div" , {"id" : "contentWrapper"})
			name_nick=content.find("div").find("h1").get_text()
			#print(char_nick)
			data=content.find("div" , {"id" : "content"})
			info=data.find("td")
			tabs=info.find_all("table", { "width":"100%" })
			#print("Animeography")
			rows=tabs[0].find_all("tr")
			for q in rows:
				anime=q.find_all("td")[1].find("a").get_text()
			#	print(anime)
				role=q.find_all("td")[1].find("small").get_text()
			#	print(role)
				ani={'anime':anime , 'role' : role }
				Animeography.append(ani)
			#print ("Mangaography")
			rows=tabs[1].find_all("tr")
			for q in rows:
				manga=q.find_all("td")[1].find("a").get_text()
			#	print(manga)
				role=q.find_all("td")[1].find("small").get_text()
			#	print(role)
				man={'manga' : manga , 'role' : role }
				Mangaography.append(man)
			bio=data.find_all("td" , { "style" : "padding-left: 5px;" })
			#print(bio[0].find("div" , { "class" : "normal_header" }).get_text())
			name_jap=bio[0].find("div" , { "class" : "normal_header" }).get_text()
			x=bio[0].find("div" , { "class" : "normal_header" }).nextSibling
			while True:
				if x.name == "div":
					if x.get_text() == "Voice Actors":
						break
					else:
						pass
				else:
					pass
				if x.name=="br":
					pass
				else:
					try:
			#			print(' '.join(x.get_text().strip().rsplit()))
						char_data=char_data+"\n"+(' '.join(x.get_text().strip().rsplit()))
					except:
			#			print(' '.join(x.strip().rsplit()))
						char_data=char_data+"\n"+(' '.join(x.strip().rsplit()))
				x=x.nextSibling
			#print (x.get_text())
			x=x.nextSibling
			#print (x.name)
			while x.name != "br":
				try:
					td=x.find_all("td")
					actor=td[1].find("a").get_text()
					language=td[1].find("small").get_text()
					act={'actor' : actor , 'language' : language}
					Voice_actors.append(act)
					#print(actor+"---"+language)
				except:
					pass
				x=x.nextSibling
			final.append([char_name,name_jap,name_nick,char_data])
			print(char_name, name_jap, name_nick , char_data )
			print()
print(final)
with open('./mangachardata.csv', 'w') as file:
	writer = csv.writer(file, delimiter=";")
	for row in final:
		writer.writerow(row)
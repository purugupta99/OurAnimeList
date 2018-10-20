import requests
from bs4 import BeautifulSoup
import csv
import base64
import os

main_url = "https://myanimelist.net/topanime.php"
req = requests.get(main_url)
htmltext = BeautifulSoup(req.content, "lxml")

final = [["Name_Anime", "Url_Char", "Name_Char",
          "Role", "Url_Actor", "Name_Actor", "Nationality"]]

pageURL = []
anime_URL = []
anime = htmltext.find_all("a", {"class": "hoverinfo_trigger fl-l fs14 fw-b"})

for i in anime:
    anime_URL.append(i['href'])
pagetxt = htmltext.find("a", {"class": "link-blue-box next"})['href']

for url in anime_URL:
    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")
    characters = source.find_all(
        "div", {"class": "detail-characters-list clearfix"})
    temp = source.find("div", {"class": "js-scrollfix-bottom"}).find_all("div")

    name_eng = (
        ' '.join(' '.join(temp[6].get_text().rsplit()).rsplit()[1:100]))
    char = characters[0].find_all("td", {"class": "borderClass"})
    
    if not os.path.exists("../static/images/characters/"+name_eng):
    	os.mkdir("../static/images/characters/"+name_eng)
    # print(img)
    #img_data = requests.get(img_url)
    #encodedImage = base64.b64encode(img_data.content)
    # print(encodedImage)
    for i in range(0, len(char), 3):
        try:
            url_char = char[i+1].contents[1]['href']
        except:
            url_char = "Not Available"

        try:
            name_char = char[i+1].contents[1].get_text()
        except:
            name_char = "Not Available"

        try:
            role = char[i+1].find("small").get_text()
        except:
            role = "Not Available"

        try:
            url_actor = char[i+2].find("a")['href']
        except:
            url_actor = "Not Available"

        try:
            name_actor = char[i+2].find("a").get_text()
        except:
            name_actor = "Not Available"

        try:
            nationality = char[i+2].find("small").get_text()
        except:
            nationality = "Not Available"

        try:
            img_actor = char[i+2].find_all("a")[1].contents[1]['data-src']
            print(img_actor)
            img_data = requests.get(img_actor)
            image_file = open("../static/images/characters/" +name_eng+"/"+name_actor+".jpg", "wb")
            for chunk in img_data.iter_content(10000):
                image_file.write(chunk)
            image_file.close()
        except:
            pass

        try:
            img_url = char[i].find("a", {"class": "fw-n"}).contents[1]['data-src']
            print(img_url)
            img_data = requests.get(img_url)
            image_file = open("../static/images/characters/" +name_eng+"/"+name_char+".jpg", "wb")
            for chunk in img_data.iter_content(10000):
                image_file.write(chunk)
            image_file.close()
        except:
        	pass
    # print(char_img)

        entry = [name_eng, url_char, name_char,
                 role, url_actor, name_actor, nationality]

        final.append(entry)

with open('./character.csv', 'w') as file:
    writer = csv.writer(file, delimiter=";")
    for row in final:
        writer.writerow(row)

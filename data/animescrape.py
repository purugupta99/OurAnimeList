import requests
from bs4 import BeautifulSoup
import csv

main_url = "https://myanimelist.net/topanime.php"
req = requests.get(main_url)
htmltext = BeautifulSoup(req.content, "lxml")

tab_gen = [["Name_Eng", "Genre"]]
final = [["Rank", "Popularity", "Score", "Name_eng", "Synonyms", "Name_Jap", "Cast_Type", "Episodes_Num", "Status", "Aired", "Premiere",
          "Broadcast", "Producers", "Licensors", "Studios", "Sources", "Genres", "Duration", "Rating", "Synopsis", "Start_Theme", "End_Theme"]]

pageURL = []
anime_URL = []
anime = htmltext.find_all("a", {"class": "hoverinfo_trigger fl-l fs14 fw-b"})

for i in anime:
    anime_URL.append(i['href'])
pagetxt = htmltext.find("a", {"class": "link-blue-box next"})['href']

for url in anime_URL:

    makers = ""
    start_theme = ""
    end_theme = ""

    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")
    rank = (source.find("span", {"class": "numbers ranked"}).find(
        "strong").contents[0])
    popularity = (source.find(
        "span", {"class": "numbers popularity"}).find("strong").contents[0])
    score = (source.find(
        "div", {"class": "fl-l score"}).contents[0].rsplit()[0])

    synopsis = (source.find("span", {"itemprop": "description"}).get_text())
    temp = source.find("div", {"class": "js-scrollfix-bottom"}).find_all("div")
    characters = source.find_all(
        "div", {"class": "detail-characters-list clearfix"})
    # print(characters)
    char = characters[0].find_all("td", {"valign": "top"}, {
                                  "class": "borderClass"})
    staff = characters[1].find_all("td", {"valign": "top"}, {
                                   "class": "borderClass"})
    #print (staff)

    open_theme = source.find(
        "div", {"class": "theme-songs js-theme-songs opnening"}).find_all("span")
    close_theme = source.find(
        "div", {"class": "theme-songs js-theme-songs ending"}).find_all("span")
    # print(open_theme)
    #print (char)
    for i in open_theme:
        start_theme += i.get_text()+","

    for i in close_theme:
        end_theme += i.get_text()+","

    for i in range(1, len(staff), 2):
        try:
            var1 = staff[i].contents[1]['href']
        except:
            var1 = ""

        try:
            var2 = staff[i].contents[1].get_text()
        except:
            var2 = ""

        try:
            var3 = staff[i].find("small").get_text()
        except:
            var3 = ""

        makers += var1+","+var2+","+var3

    p = 6
    name_eng = (
        ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
    p += 1
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Synonyms:"):
        synonyms = (
            ' '.join(' '.join(temp[7].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        synonyms = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Japanese:"):
        name_jap = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        name_jap = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Type:"):
        cast_type = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        cast_type = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Episodes:"):
        episodes_num = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        episodes_num = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Status:"):
        status = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        status = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Aired:"):
        aired = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        aired = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Premiered:"):
        premiere = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        premiere = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Broadcast:"):
        broadcast = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        broadcast = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Producers:"):
        producers = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        producers = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Licensors:"):
        licensors = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        licensors = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Studios:"):
        studios = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        studios = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Source:"):
        sources = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        sources = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Genres:"):
        genres = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        genres = []
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Duration:"):
        duration = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
        p += 1
    else:
        duration = ""
    if(' '.join(temp[p].get_text().rsplit()).rsplit()[0] == "Rating:"):
        rating = (
            ' '.join(' '.join(temp[p].get_text().rsplit()).rsplit()[1:100]))
    else:
        rating = ""

    img_url = source.find("div", {"id": "content"}).find("img")['src']
    img_data = requests.get(img_url)
    #print(img_data.content)
    image_file = open("../static/images/cover/"+name_eng+".jpg", "wb")
    for chunk in img_data.iter_content(10000):
        image_file.write(chunk)
    image_file.close()

    for g in (genres.rsplit(',')):
        entry_gen = [name_eng, g.rsplit()[0]]
        # print(entry_gen)
        tab_gen.append(entry_gen)
    # voice, makers not included
    entry = [rank[1:], popularity[1:], score, name_eng, synonyms, name_jap, cast_type, episodes_num, status, aired, premiere,
             broadcast, producers, licensors, studios, sources, genres, duration, rating, synopsis, start_theme, end_theme]
    final.append(entry)

with open('./main.csv', 'w') as file:
    writer = csv.writer(file, delimiter=";")
    for row in final:
        writer.writerow(row)
    file.close()

with open('./genre.csv', 'w') as file:
    writer = csv.writer(file, delimiter=";")
    for row in tab_gen:
        writer.writerow(row)
    file.close()

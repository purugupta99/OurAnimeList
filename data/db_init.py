import sqlite3
import csv

con = sqlite3.connect('anime.db')

def reader():
	cur = con.cursor()
	reader = csv.reader(open('main.csv','r'),delimiter=';')
	for row in reader:
		to_db = [unicode(row[0], "utf8"),unicode(row[1], "utf8"),unicode(row[2], "utf8"),unicode(row[3], "utf8"),unicode(row[4], "utf8"),unicode(row[5], "utf8"),unicode(row[6], "utf8"),unicode(row[7], "utf8"),unicode(row[8], "utf8"),unicode(row[9], "utf8"),unicode(row[10], "utf8"),unicode(row[11], "utf8"),unicode(row[12], "utf8"),unicode(row[13], "utf8"),unicode(row[14], "utf8"),unicode(row[15], "utf8"),unicode(row[16], "utf8"),unicode(row[17], "utf8"),unicode(row[18], "utf8"),unicode(row[19], "utf8"),unicode(row[20], "utf8"),unicode(row[21], "utf8")]
		cur.execute("INSERT INTO anime (RANK,POPULARITY,SCORE,NAME_ENG,SYNONYMS,NAME_JAP,CAST_TYPE,EPISODES_NUM,STATUS,AIRED,PREMIERE,BROADCAST,PRODUCERS,LICENSORS,STUDIOS,SOURCES,GENRES,DURATION,RATING,SYNOPSIS,START_THEME,END_THEME) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",to_db)
	con.commit()

	reader = csv.reader(open('character.csv','r'),delimiter=';')
	for row in reader:
		to_db = [unicode(row[0], "utf8"),unicode(row[1], "utf8"),unicode(row[2], "utf8"),unicode(row[3], "utf8"),unicode(row[4], "utf8"),unicode(row[5], "utf8"),unicode(row[6], "utf8")]
		cur.execute("INSERT INTO characters (NAME_ENG,URL_CHAR,NAME_CHAR,ROLE,URL_ACTOR,NAME_ACTOR,NATIONALITY) VALUES (?,?,?,?,?,?,?);",to_db)
	con.commit()

	reader = csv.reader(open('genre.csv','r'),delimiter=';')
	for row in reader:
		to_db = [unicode(row[0], "utf8"),unicode(row[1], "utf8")]
		cur.execute("INSERT INTO anime_genre (NAME_ENG,GENRES) VALUES (?,?);",to_db)
	con.commit()

reader()
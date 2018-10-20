from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin, current_user, login_required
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeSerializer
from flask_uploads import UploadSet, configure_uploads, IMAGES
from math import floor
import csv
import os
from datetime import datetime, timedelta
from model import *
app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
UPLOAD_FOLDER = 'static/profilepics'

engine = create_engine('sqlite:///anime.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./anime.db'
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOADED_PHOTOS_DEST'] = 'static/profilepics'

#configure_uploads(app, photos)

serializer = URLSafeSerializer(app.secret_key)
db = SQLAlchemy(app)

def try_except(func):
    def wrapper(*kwargs):
        try:
            func(*kwargs)
        except:
            pass
    return wrapper
# csv_reader('~/Assignments/ITWS-II/OurAnimeList/data/main.csv',Anime)
# csv_reader('~/Assignments/ITWS-II/OurAnimeList/data/character.csv',Characters)
# csv_reader('~/Assignments/ITWS-II/OurAnimeList/data/genre.csv',Anime_Genre)


flag=0
file = open('genre.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        result = Anime.query.filter_by(name_eng=row[0]).first()
        record = Anime_Genre(name_eng=row[0],genres=row[1],anime=result)
        db.session.add(record)
        db.session.commit()
    flag=flag+1

flag = 0
file = open('main.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        record = Anime(id=flag,name_eng=row[3],synonyms=row[4],name_jap=row[5],cast_type=row[6],episodes_num=row[7],status=row[8],aired=row[9],premiere=row[10],broadcast=row[11],producers=row[12],licensors=row[13],studios=row[14],sources=row[15],genres=row[16],duration=row[17],rating=row[18],synopsis=row[19],start_theme=row[20],end_theme=row[21])
        db.session.add(record)
        db.session.commit()
    flag = flag + 1


flag=0
file = open('mangadata.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        if row[8]=="Unknown":
            row[8]=-1
        if row[9]=="Unknown":
            row[9]=-1
        record = Manga(id=flag,rank=row[0],popularity=row[1],score=float(row[2]),name_eng=row[3],altername_eng=row[4],synonyms=row[5],name_jap=row[6],cast_type=row[7],volumes_num=row[8],chapters_num=row[9],status=row[10],published=row[11],genres=row[12],authors=row[13],serialization=row[14],synopsis=row[15])
        db.session.add(record)
        db.session.commit()
    flag=flag+1

flag=0
file = open('genremanga.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        record = Manga_Genre(id=flag,name_eng=row[0],genres=row[1])
        db.session.add(record)
        db.session.commit()
    flag=flag+1

flag=0
file = open('mangachars.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        result = Manga.query.filter_by(name_eng=row[0]).first()
        record = Characters_Manga(name_manga=row[0],url_char=row[3],name_char=row[1],role=row[2],manga=result)
        db.session.add(record)
        db.session.commit()

    flag = flag + 1

flag=0
file = open('mangachardata.csv','r')
reader = csv.reader(file,delimiter=";")
for row in reader:
    if flag > 0:
        print(row)
        result = Characters_Manga.query.filter_by(name_char=row[0]).all()
        print(result)
        for res in result:
            res.name_jap = row[1]
            res.nick = row[2]
            res.data = row[3]
            db.session.merge(res)
            db.session.commit()
    flag = flag + 1

loop = Manga.query.all()
for i in loop:
    entry = Score_Manga(manga_name=i.name_eng,manga_id=i.id)
    db.session.add(entry)
db.session.commit()

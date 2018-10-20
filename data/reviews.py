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
from data.anime import *
from data.manga import *
from data.database_init import *


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





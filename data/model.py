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

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    bio = db.Column(db.String)
    gender = db.Column(db.String)
    profilepic = db.Column(db.Boolean)
    verify_token = db.Column(db.String)
    verified = db.Column(db.Boolean)
    session_token = db.Column(db.String(100), unique=True)
    privilage=db.Column(db.Boolean,default=False)
    anime_list = db.relationship("Anime_List", backref="user", passive_deletes=True)
    #anime_review = db.relationship("Review", backref="anime_review_user", passive_deletes=True)
    #anime_recommend = db.relationship("Recommendation", backref="anime_rec_user", passive_deletes=True)
    manga_list=db.relationship("Manga_List" , backref="manga_user" , passive_deletes=True )
    manga_review = db.relationship("Review_Manga", backref="manga_review_user", passive_deletes=True)
    manga_recommend = db.relationship("Recommendation_Manga", backref="manga_rec_user", passive_deletes=True)


    def get_id(self):
        return str(self.session_token)

    def create_user(name, username, email, password,token):
        password = sha256_crypt.encrypt(password)
        user = User(name=name, username=username, email=email, password=password, bio="None",
                    gender="None", profilepic=False, verify_token=token, verified=False ,session_token=serializer.dumps([username, password]))
        db.session.add(user)
        db.session.commit()
    
    def display_user():
        result = User.query.all()
        users = []
        for user in result:
            dictionary = {
                "name" : user.name,
                "username" : user.username,
                "email" : user.email
            }
            users.append(dictionary)
        return users

    @try_except
    def delete_user():
        username = request.form['del_username']
        #anime_list = Anime_List.query.filter_by(username=username).all()
        #review = Review.query.filter_by(username=username).all()
        #recommendation = Recommendation.query.filter_by(username=username).all()
        #print (username)
        Anime_List.query.filter_by(username=username).delete()
        User.query.filter_by(username=username).delete()
        Review.query.filter_by(username=username).delete()
        Recommendation.query.filter_by(username=username).delete()
        db.session.commit()

    @try_except
    @login_required
    def change_bio():
        bio = request.form['bio']
        pwd = current_user.password
        password = request.form['passwd3']
        status = sha256_crypt.verify(password, pwd)
        if status:
            current_user.bio = bio
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect!!")

    @try_except
    @login_required
    def change_name():
        name = request.form['name']
        pwd = current_user.password
        password = request.form['passwd1']
        status = sha256_crypt.verify(password, pwd)
        if status:
            current_user.name = name
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect!!")

    @try_except
    @login_required
    def change_email():
        email = request.form['email']
        pwd = current_user.password
        password = request.form['passwd2']
        status = sha256_crypt.verify(password, pwd)
        if status:
            current_user.email = email
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect!!")

    @try_except
    @login_required
    def change_email():
        email = request.form['email']
        pwd = current_user.password
        password = request.form['passwd2']
        status = sha256_crypt.verify(password, pwd)
        if status:
            current_user.email = email
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect!!")

    @try_except
    @login_required
    def change_gender():
        gender = request.form['gender']
        pwd = current_user.password
        password = request.form['passwd4']
        status = sha256_crypt.verify(password, pwd)
        if status:
            current_user.gender = gender
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect!!")

    @try_except
    @login_required
    def change_password():
        currpasswd = request.form['currpasswd']
        newpasswd = request.form['newpasswd']
        repasswd = request.form['repasswd']
        pwd = current_user.password
        status = sha256_crypt.verify(currpasswd, pwd)
        if not status:
            #print("Current Password is Incorrect")
            flash("Current Password is Incorrect")

        if newpasswd != repasswd:
            #print("Re-Enter your New Password")
            flash("Re-Enter your New Password")

        if status and newpasswd == repasswd:
            newpasswd = sha256_crypt.encrypt(newpasswd)
            current_user.password = newpasswd
            current_user.session_token = serializer.dumps([username, password])
            db.session.merge(current_user)
            db.session.commit()

    @try_except
    @login_required
    def upload():
        password = request.form['passwd5']
        pwd = current_user.password
        status = sha256_crypt.verify(password, pwd)
        if status:
            # print(UPLOAD_FOLDER,current_user.username)
            if current_user.profilepic == True:
                os.system("rm {}/{}.jpeg".format(UPLOAD_FOLDER,
                                                current_user.username))
            #print ("rm {}/{}.jpg".format(UPLOAD_FOLDER,current_user.username))
            photos.save(request.files['profilepic'],
                        None, current_user.username+".")
            current_user.profilepic = True
            db.session.merge(current_user)
            db.session.commit()
        else:
            flash("Password is incorrect")


class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, default=1)
    #popularity = db.Column(db.Integer)
    #score = db.Column(db.Float)
    name_eng = db.Column(db.String)
    synonyms = db.Column(db.String)
    name_jap = db.Column(db.String)
    cast_type = db.Column(db.String)
    episodes_num = db.Column(db.Integer)
    status = db.Column(db.String)
    aired = db.Column(db.String)
    premiere = db.Column(db.String)
    broadcast = db.Column(db.String)
    producers = db.Column(db.String)
    licensors = db.Column(db.String)
    studios = db.Column(db.String)
    sources = db.Column(db.String)
    genres = db.Column(db.String)
    duration = db.Column(db.String)
    rating = db.Column(db.String)
    synopsis = db.Column(db.String)
    start_theme = db.Column(db.String)
    end_theme = db.Column(db.String)
    characters = db.relationship('Characters', backref='anime', passive_deletes=True)
    genre = db.relationship('Anime_Genre', backref='anime', passive_deletes=True)
    #recommendation = db.relationship('Recommendation', backref='anime', passive_deletes=True)
    
    @try_except
    @login_required
    def add_anime():
        name_eng = request.form['name_eng']
        name_jap = request.form['name_jap']
        synonyms = request.form['synonyms']
        cast_type = request.form['cast_type']
        episodes_num = int(request.form['episodes_num'])
        status = request.form['status']
        aired = request.form['aired']
        premiered = request.form['premiered']
        broadcast = request.form['broadcast']
        producers = request.form['producers']
        licensors = request.form['licensors']
        studios = request.form['studio']
        sources = request.form['source']
        duration = request.form['duration']
        genres = request.form['genres']
        char_num = int(request.form['char_num'])
        synopsis = request.form['synopsis']
        rating=request.form['rating']
        anime = Anime(name_eng=name_eng,rank=100,synonyms=synonyms,rating=rating,name_jap=name_jap,cast_type=cast_type,episodes_num=episodes_num,status=status,aired=aired,premiere=premiered,broadcast=broadcast,producers=producers,licensors=licensors,studios=studios,sources=sources,genres=genres,duration=duration,synopsis=synopsis)
        db.session.add(anime)
        anime_id=Anime.query.filter_by(name_eng=name_eng).first().id
        score=Score_Anime(anime_name=name_eng,anime_id=anime_id)
        db.session.add(score)

        if char_num > 0:
            char1_name = request.form['char1_name']
            char1_role = request.form['char1_role']
            act1_name = request.form['act1_name']
            act1_language = request.form['act1_language']
            char1_data = request.form['char1_data']
            char1 = Characters(anime=anime,name_anime=name_eng,name_char=char1_name,role=char1_role,name_actor=act1_name,nationality=act1_language,data=char1_data,nick=char1_name)
            db.session.add(char1)
        
        if char_num > 1:
            char2_name = request.form['char2_name']
            char2_role = request.form['char2_role']
            act2_name = request.form['act2_name']
            act2_language = request.form['act2_language']
            char2_data = request.form['char2_data']
            char2 = Characters(anime=anime,name_anime=name_eng,name_char=char2_name,role=char2_role,name_actor=act2_name,nationality=act2_language,data=char2_data,nick=char2_name)
            db.session.add(char2)

        if char_num > 2:
            char3_name = request.form['char3_name']
            char3_role = request.form['char3_role']
            act3_name = request.form['act3_name']
            act3_language = request.form['act3_language']
            char3_data = request.form['char3_data']
            char3 = Characters(anime=anime,name_anime=name_eng,name_char=char3_name,role=char3_role,name_actor=act3_name,nationality=act3_language,data=char3_data,nick=char3_name)
            db.session.add(char3)

        if char_num > 3:
            char4_name = request.form['char4_name']
            char4_role = request.form['char4_role']
            act4_name = request.form['act4_name']
            act4_language = request.form['act4_language']
            char4_data = request.form['char4_data']
            char4 = Characters(anime=anime,name_anime=name_eng,name_char=char4_name,role=char4_role,name_actor=act4_name,nationality=act4_language,data=char4_data,nick=char4_name)
            db.session.add(char4)

        if char_num > 4:
            char5_name = request.form['char5_name']
            char5_role = request.form['char5_role']
            act5_name = request.form['act5_name']
            act5_language = request.form['act5_language']
            char5_data = request.form['char5_data']
            char5 = Characters(anime=anime,name_anime=name_eng,name_char=char5_name,role=char5_role,name_actor=act5_name,nationality=act5_language,data=char5_data,nick=char5_name)
            db.session.add(char5)

        if char_num > 5:
            char6_name = request.form['char6_name']
            char6_role = request.form['char6_role']
            act6_name = request.form['act6_name']
            act6_language = request.form['act6_language']
            char6_data = request.form['char6_data']
            char6 = Characters(anime=anime,name_anime=name_eng,name_char=char6_name,role=char6_role,name_actor=act6_name,nationality=act6_language,data=char6_data,nick=char6_name)
            db.session.add(char6)

        if char_num > 6:
            char7_name = request.form['char7_name']
            char7_role = request.form['char7_role']
            act7_name = request.form['act7_name']
            act7_language = request.form['act7_language']
            char7_data = request.form['char7_data']
            char7 = Characters(anime=anime,name_anime=name_eng,name_char=char7_name,role=char7_role,name_actor=act7_name,nationality=act7_language,data=char7_data,nick=char7_name)
            db.session.add(char7)

        if char_num > 7:
            char8_name = request.form['char8_name']
            char8_role = request.form['char8_role']
            act8_name = request.form['act8_name']
            act8_language = request.form['act8_language']
            char8_data = request.form['char8_data']
            char8 = Characters(anime=anime,name_anime=name_eng,name_char=char8_name,role=char8_role,name_actor=act8_name,nationality=act8_language,data=char8_data,nick=char8_name)
            db.session.add(char8)

        db.session.commit()
        print(name_eng)

    def top_rank():
        result = Anime.query.order_by(Anime.rank).limit(11).all()
        result = result[:10]
        #print(result)
        return result

    def update_rank():
        result=Score_Anime.query.order_by(Score_Anime.total_score.desc()).all()
        #print(result)
        rank = 1
        for anime in result:
            anime_obj = Anime.query.filter_by(id=anime.anime_id).first()
            #print(anime_obj)
            anime_obj.rank = rank
            rank+=1
        db.session.commit()


    def display_anime():
        result = Anime.query.all()
        anime = []
        for i in result:
            dictionary = {
                "id" : i.id,
                "name" : i.name_eng,
                "status" : i.status,
                "type" : i.cast_type,
                "studios" : i.studios,
            }
            anime.append(dictionary)
        return anime

    @try_except
    def delete_anime():
        #print (request.form)
        anime_id = request.form['anime_id']
        #print(anime_id)
        name = Anime.query.filter_by(id=anime_id).first().name_eng
        #print(name)
        Anime.query.filter_by(id=anime_id).delete()
        Review.query.filter_by(anime=name).delete()
        User_Score.query.filter_by(anime_name=name).delete()
        Characters.query.filter_by(name_anime=name).delete()
        Recommendation.query.filter_by(anime=name).delete()
        Anime_Genre.query.filter_by(name_eng=name).delete()
        Anime_List.query.filter_by(anime=name).delete()
        db.session.commit()

class User_Score(db.Model):
    __tablename__ = 'user_score'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    anime_name = db.Column(db.String)
    score = db.Column(db.Integer)
    anime_id = db.Column(db.Integer)

class Anime_List(db.Model):
    __tablename__ = 'anime_list'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    status = db.Column(db.String)
    anime = db.Column(db.String)
    rewatched = db.Column(db.Integer)
    episodes_num = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'))

    @try_except
    @login_required
    def add_anime():
        username = current_user.username
        status = request.form['status']
        anime = request.form['anime']
        rewatched = int(request.form['rewatch'])
        episodes_num = int(request.form['episode'])
        result = Anime_List.query.filter_by(username=username, anime=anime).first()
        if result:
            result.status=status
            result.rewatched=rewatched
            result.episodes_num=episodes_num
            if status == "Completed":
                result.episodes_num = request.form['completed']
            db.session.merge(result)
            #print ("result ",result)
        else:
            if status == "Completed":
                episodes_num = request.form['completed']
            entry = Anime_List(username=username,status=status,anime=anime,rewatched=rewatched,episodes_num=episodes_num,user=current_user)
            db.session.add(entry)
            #print("entry ",entry)
        db.session.commit()

    def get_anime_user(username):
        result_rewatch = Anime_List.query.filter_by(username=username).all()
        result_watching = len(Anime_List.query.filter_by(username=username, status="Watching").all())
        result_completed = len(Anime_List.query.filter_by(username=username, status="Completed").all())
        result_onhold = len(Anime_List.query.filter_by(username=username, status="On-Hold").all())
        result_dropped = len(Anime_List.query.filter_by(username=username, status="Dropped").all())
        result_plan = len(Anime_List.query.filter_by(username=username, status="Plan to Watch").all())
        total = len(result_rewatch)
        rewatch = 0
        episode = 0
        for entry in result_rewatch:
            rewatch = entry.rewatched + rewatch
            if entry.rewatched > 0:
                episode += Anime.query.filter_by(name_eng=entry.anime).first().episodes_num
                #print(Anime.query.filter_by(name_eng=entry.anime).first().genre)
            else:
                episode += entry.episodes_num
        dictionary = {
            "watching" : result_watching,
            "completed" : result_completed,
            "onhold" : result_onhold,
            "dropped" : result_dropped,
            "planned" : result_plan,
            "total" : total,
            "rewatch" : rewatch,
            "episode" : episode,
        }
        #print (result_watching,result_plan,result_dropped,result_onhold,result_completed)
        return(dictionary)

    def get_anime(anime):
        result_rewatch = Anime_List.query.filter_by(anime=anime).all()
        result_watching = len(Anime_List.query.filter_by(anime=anime, status="Watching").all())
        result_completed = len(Anime_List.query.filter_by(anime=anime, status="Completed").all())
        result_onhold = len(Anime_List.query.filter_by(anime=anime, status="On-Hold").all())
        result_dropped = len(Anime_List.query.filter_by(anime=anime, status="Dropped").all())
        result_plan = len(Anime_List.query.filter_by(anime=anime, status="Plan to Watch").all())
        total = len(result_rewatch)
        
        dictionary = {
            "watching" : result_watching,
            "completed" : result_completed,
            "onhold" : result_onhold,
            "dropped" : result_dropped,
            "planned" : result_plan,
            "total" : total,
        }
        #print (result_watching,result_plan,result_dropped,result_onhold,result_completed)
        return(dictionary)

    def user_list(username):
        result = Anime_List.query.filter_by(username=username).all()
        if result:
            listing = []
            for i in result:
                anime_result = Anime.query.filter_by(name_eng=i.anime).first()
                score_result = Score_Anime.query.filter_by(anime_name=i.anime).first()
                dictionary = {
                    "anime" : i.anime,
                    "anime_id" : anime_result.id,
                    "episodes" : anime_result.episodes_num,
                    "type" : anime_result.cast_type,
                    "score" : score_result.total_score,
                    "members" : score_result.total,
                    "synopsis" : anime_result.synopsis[:400] + "...",
                    "status" : i.status,
                    "episodes_watched" : i.episodes_num,
                    "rewatched" : i.rewatched
                }
                listing.append(dictionary)
            return listing

    @try_except
    @login_required
    def delete_list():
        anime = request.form['del_list_anime']
        result = Anime_List.query.filter_by(anime=anime, username=current_user.username).delete()
        db.session.commit()

    @login_required
    def suggested_anime():
        anime_list = User_Score.query.filter_by(username=current_user.username).order_by(User_Score.score.desc()).limit(3).all()
        all_anime=Anime.query.all()
        result=[]
        count=0
        for i in anime_list:
            anime=Anime.query.filter_by(name_eng=i.anime_name).first()
            genres_anime=anime.genres.rsplit(',')
            for animes in all_anime:
                c=0
                for a in anime_list:
                    ap=Anime.query.filter_by(name_eng=a.anime_name).first()
                    if animes.name_eng == ap.name_eng:
                        c=1
                if c==1:
                    continue
                count=0
                genres_animes=animes.genres.rsplit(',')
                for genre1 in genres_anime:
                    for genre2 in genres_animes:
                        if genre2==genre1:
                            count+=1
                if count>6:
                    result.append(animes)
        result.sort(key=lambda x : x.rank )
        return result[:3]


class Score_Anime(db.Model):
    __tablename__ = 'score_anime'
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer)
    anime_name = db.Column(db.String)
    score_1 = db.Column(db.Integer, default=0)
    score_2 = db.Column(db.Integer, default=0)
    score_3 = db.Column(db.Integer, default=0)
    score_4 = db.Column(db.Integer, default=0)
    score_5 = db.Column(db.Integer, default=0)
    score_6 = db.Column(db.Integer, default=0)
    score_7 = db.Column(db.Integer, default=0)
    score_8 = db.Column(db.Integer, default=0)
    score_9 = db.Column(db.Integer, default=0)
    score_10 = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Float, default=0)

    @try_except
    @login_required
    def update_score():
        user = current_user.username
        score = int(request.form['score'])
        anime_name = request.form['anime_name']
        result = User_Score.query.filter_by(username=user, anime_name=anime_name).first()
        final = Score_Anime.query.filter_by(anime_name=anime_name).first()
        if result:
            temp = result.score
            result.score = score
            total = (final.total_score*final.total - temp + score)/final.total
            if temp==1:
                final.score_1-=1
            elif temp==2:
                final.score_2-=1
            elif temp==3:
                final.score_3-=1
            elif temp==4:
                final.score_4-=1
            elif temp==5:
                final.score_5-=1
            elif temp==6:
                final.score_6-=1
            elif temp==7:
                final.score_7-=1
            elif temp==8:
                final.score_8-=1
            elif temp==9:
                final.score_9-=1
            elif temp==10:
                final.score_10-=1


            if score==1:
                final.score_1+=1
            elif score==2:
                final.score_2+=1
            elif score==3:
                final.score_3+=1
            elif score==4:
                final.score_4+=1
            elif score==5:
                final.score_5+=1
            elif score==6:
                final.score_6+=1
            elif score==7:
                final.score_7+=1
            elif score==8:
                final.score_8+=1
            elif score==9:
                final.score_9+=1
            elif score==10:
                final.score_10+=1

            final.total_score = total
            db.session.merge(result)
            db.session.merge(final)
            db.session.commit()
        else:
            if score==1:
                final.score_1+=1
            elif score==2:
                final.score_2+=1
            elif score==3:
                final.score_3+=1
            elif score==4:
                final.score_4+=1
            elif score==5:
                final.score_5+=1
            elif score==6:
                final.score_6+=1
            elif score==7:
                final.score_7+=1
            elif score==8:
                final.score_8+=1
            elif score==9:
                final.score_9+=1
            elif score==10:
                final.score_10+=1
            final.total+=1
            final.total_score = (final.total_score+score)/final.total 
            anime_id = Anime.query.filter_by(name_eng=anime_name).first().id
            entry = User_Score(username=user,anime_name=anime_name,score=score,anime_id=anime_id)
            db.session.add(entry)
            db.session.merge(final)
            db.session.commit()
        Anime.update_rank()


    def best(username):
        lis=User_Score.query.filter_by(username=username).order_by(User_Score.score.desc()).limit(6).all()
        ans=[]
        for i in lis:
            dic={
            'name' :i.anime_name,
            "id" : i.anime_id,
            "score" : i.score,
            }
            ans.append(dic)
        return ans
            


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name_anime = db.Column(db.String)
    url_char = db.Column(db.String)
    name_char = db.Column(db.String)
    name_jap = db.Column(db.String)
    role = db.Column(db.String)
    url_actor = db.Column(db.String)
    name_actor = db.Column(db.String)
    nationality = db.Column(db.String)
    data = db.Column(db.String)
    nick = db.Column(db.String)
    anime_id = db.Column(db.Integer,db.ForeignKey('anime.id', ondelete='CASCADE'))

    def get_charac(num):
        result = Characters.query.filter_by(id=num).first()
        result_2 = Characters.query.filter_by(name_char=result.name_char).all()
        #anime = Anime.query.filter_by(name_eng=result.name_anime).first().id
        anime_name=[]
        for res in result_2:
            try:
                anime = Anime.query.filter_by(name_eng=res.name_anime).first().id
            except:
                anime=5000
            dicta={
            'name' : res.name_anime,
            'id' : anime,
            'role' : res.role,
            }
            anime_name.append(dicta)

        data = {
            "animeography" : anime_name,
            "name_char" : result.name_char,
            "name_jap" : result.name_jap,
            "name_actor" : result.name_actor,
            "nationality" : result.nationality,
            "data" : result.data,
            "nick" : result.nick,
        }
        return data


class Anime_Genre(db.Model):
    __tablename__ = 'anime_genre'
    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String)
    genres = db.Column(db.String)
    anime_id = db.Column(db.Integer,db.ForeignKey('anime.id', ondelete='CASCADE'))


class Manga(db.Model):
    __tablename__ = 'manga'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    score = db.Column(db.Float)
    name_eng = db.Column(db.String)
    altername_eng = db.Column(db.String)
    synonyms = db.Column(db.String)
    name_jap = db.Column(db.String)
    cast_type = db.Column(db.String)
    volumes_num = db.Column(db.Integer)
    chapters_num = db.Column(db.Integer)
    status = db.Column(db.String)
    published = db.Column(db.String)
    genres = db.Column(db.String)
    authors = db.Column(db.String)
    serialization = db.Column(db.String)
    synopsis = db.Column(db.String)
    characters = db.relationship('Characters_Manga', backref='manga' , passive_deletes=True)

    @try_except
    @login_required
    def add_manga():
        name_eng = request.form['name_eng']
        altername_eng=request.form['altername_eng']
        name_jap = request.form['name_jap']
        synonyms = request.form['synonyms']
        cast_type = request.form['cast_type']
        volumes_num = int(request.form['volumes_num'])
        chapters_num = int(request.form['chapters_num'])
        status = request.form['status']
        published = request.form['published']
        authors = request.form['authors']
        serialization = request.form['serialization']
        genres = request.form['genres']
        char_num = int(request.form['char_num'])
        synopsis = request.form['synopsis']
        manga = Manga(name_eng=name_eng,rank=100,synonyms=synonyms,altername_eng=altername_eng,name_jap=name_jap,cast_type=cast_type,volumes_num=volumes_num,chapters_num=chapters_num,status=status,published=published,authors=authors,serialization=serialization,genres=genres,synopsis=synopsis)
        db.session.add(manga)
        manga_id=Manga.query.filter_by(name_eng=name_eng).first().id
        score=Score_Manga(manga_name=name_eng,manga_id=manga_id)
        db.session.add(score)

        if char_num > 0:
            char1_name = request.form['char1_name']
            char1_role = request.form['char1_role']
            char1_data = request.form['char1_data']
            char1 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char1_name,role=char1_role,data=char1_data,nick=char1_name)
            db.session.add(char1)
        
        if char_num > 1:
            char2_name = request.form['char2_name']
            char2_role = request.form['char2_role']
            char2_data = request.form['char2_data']
            char2 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char2_name,role=char2_role,data=char2_data,nick=char2_name)
            db.session.add(char2)

        if char_num > 2:
            char3_name = request.form['char3_name']
            char3_role = request.form['char3_role']
            char3_data = request.form['char3_data']
            char3 = Characters(manga=manga,name_manga=name_eng,name_char=char3_name,role=char3_role,data=char3_data,nick=char3_name)
            db.session.add(char3)

        if char_num > 3:
            char4_name = request.form['char4_name']
            char4_role = request.form['char4_role']
            char4_data = request.form['char4_data']
            char4 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char4_name,role=char4_role,data=char4_data,nick=char4_name)
            db.session.add(char4)

        if char_num > 4:
            char5_name = request.form['char5_name']
            char5_role = request.form['char5_role']
            char5_data = request.form['char5_data']
            char5 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char5_name,role=char5_role,data=char5_data,nick=char5_name)
            db.session.add(char5)

        if char_num > 5:
            char6_name = request.form['char6_name']
            char6_role = request.form['char6_role']
            char6_data = request.form['char6_data']
            char6 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char6_name,role=char6_role,data=char6_data,nick=char6_name)
            db.session.add(char6)

        if char_num > 6:
            char7_name = request.form['char7_name']
            char7_role = request.form['char7_role']
            char7_data = request.form['char7_data']
            char7 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char7_name,role=char7_role,data=char7_data,nick=char7_name)
            db.session.add(char7)

        if char_num > 7:
            char8_name = request.form['char8_name']
            char8_role = request.form['char8_role']
            char8_data = request.form['char8_data']
            char8 = Characters_Manga(manga=manga,name_manga=name_eng,name_char=char8_name,role=char8_role,data=char8_data,nick=char8_name)
            db.session.add(char8)

        db.session.commit()

    def top_rank():
        result = Manga.query.order_by(Manga.rank).limit(11).all()
        result = result[:10]
        #print(result)
        return result

    def update_rank():
        result=Score_Manga.query.order_by(Score_Manga.total_score.desc()).all()
        #print(result)
        rank = 1
        for manga in result:
            manga_obj = Manga.query.filter_by(id=manga.manga_id).first()
            #print(manga_obj)
            manga_obj.rank = rank
            rank+=1
        db.session.commit()


    def display_manga():
        result = Manga.query.all()
        manga = []
        for i in result:
            dictionary = {
                "id" : i.id,
                "name" : i.name_eng,
                "status" : i.status,
                "type" : i.cast_type,
                "serialization" : i.serialization,
            }
            manga.append(dictionary)
        return manga

    @try_except
    @login_required
    def delete_manga():
        #print (request.form)
        manga_id = request.form['manga_id']
        #print(anime_id)
        name = Manga.query.filter_by(id=manga_id).first().name_eng
        #print(name)
        Manga.query.filter_by(id=manga_id).delete()
        Review_Manga.query.filter_by(manga=name).delete()
        Characters_Manga.query.filter_by(name_manga=name).delete()
        Recommendation_Manga.query.filter_by(manga=name).delete()
        Recommendation_Manga.query.filter_by(recommended_manga=name).delete()
        User_Score_Manga.query.filter_by(manga_name=name).delete()
        Manga_Genre.query.filter_by(name_eng=name).delete()
        Manga_List.query.filter_by(manga=name).delete()
        db.session.commit()

class Manga_Genre(db.Model):
    __tablename__ = 'manga_genre'
    id = db.Column(db.Integer, primary_key=True)
    name_eng = db.Column(db.String, db.ForeignKey('manga.name_eng'))
    genres = db.Column(db.String)

class Manga_List(db.Model):
    __tablename__ = 'manga_list'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    status = db.Column(db.String)
    manga = db.Column(db.String)
    reread = db.Column(db.Integer)
    volumes_num = db.Column(db.Integer)
    chapters_num = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE'))

    @try_except
    @login_required
    def add_manga():
        username = current_user.username
        status = request.form['status']
        manga = request.form['manga']
        reread = int(request.form['reread'])
        chapters_num = int(request.form['chapter'])
        volumes_num = int(request.form['volume'])
        result = Manga_List.query.filter_by(username=username, manga=manga).first()
        if result:
            result.status=status
            result.reread=reread
            result.volumes_num = volumes_num
            result.chapters_num = chapters_num
            if status == "Completed":
                result.volumes_num = request.form['volumes_num']
                result.chapters_num = request.form['chapters_num']
            db.session.merge(result)
            #print ("result ",result)
        else:
            if status == "Completed":
                volumes_num = request.form['volumes_num']
                chapters_num = request.form['chapters_num']
            entry = Manga_List(username=username,status=status,manga=manga,reread=reread,chapters_num=chapters_num,volumes_num=volumes_num,manga_user=current_user)
            db.session.add(entry)
            #print("entry ",entry)
        db.session.commit()

    def get_manga_user(username):
        result_reread = Manga_List.query.filter_by(username=username).all()
        result_reading = len(Manga_List.query.filter_by(username=username, status="Reading").all())
        result_completed = len(Manga_List.query.filter_by(username=username, status="Completed").all())
        result_onhold = len(Manga_List.query.filter_by(username=username, status="On-Hold").all())
        result_dropped = len(Manga_List.query.filter_by(username=username, status="Dropped").all())
        result_plan = len(Manga_List.query.filter_by(username=username, status="Plan to Read").all())
        total = len(result_reread)
        reread = 0
        chapters = 0
        volumes = 0
        for entry in result_reread:
            reread = entry.reread + reread
            if entry.reread > 0:
                chapters += Manga.query.filter_by(name_eng=entry.manga).first().chapters_num
                volumes += Manga.query.filter_by(name_eng=entry.manga).first().volumes_num
                #print(Anime.query.filter_by(name_eng=entry.anime).first().genre)
            else:
                if entry.chapters_num > 0:
                    chapters += entry.chapters_num
                if entry.volumes_num>0 :
                    volumes += entry.volumes_num
        dictionary = {
            "reading" : result_reading,
            "completed" : result_completed,
            "onhold" : result_onhold,
            "dropped" : result_dropped,
            "planned" : result_plan,
            "total" : total,
            "reread" : reread,
            "chapter" : chapters,
            "volume" : volumes,
        }
        #print (result_watching,result_plan,result_dropped,result_onhold,result_completed)
        return(dictionary)

    def get_manga(manga):
        result_reread = Manga_List.query.filter_by(manga=manga).all()
        result_reading = len(Manga_List.query.filter_by(manga=manga, status="Reading").all())
        result_completed = len(Manga_List.query.filter_by(manga=manga, status="Completed").all())
        result_onhold = len(Manga_List.query.filter_by(manga=manga, status="On-Hold").all())
        result_dropped = len(Manga_List.query.filter_by(manga=manga, status="Dropped").all())
        result_plan = len(Manga_List.query.filter_by(manga=manga, status="Plan to Read").all())
        total = len(result_reread)
        
        dictionary = {
            "reading" : result_reading,
            "completed" : result_completed,
            "onhold" : result_onhold,
            "dropped" : result_dropped,
            "planned" : result_plan,
            "total" : total,
        }
        #print (result_reading,result_plan,result_dropped,result_onhold,result_completed)
        return(dictionary)

    def user_list(username):
        result = Manga_List.query.filter_by(username=username).all()
        if result:
            listing = []
            for i in result:
                manga_result = Manga.query.filter_by(name_eng=i.manga).first()
                #score_result = Score_Anime.query.filter_by(anime_name=i.anime).first()
                dictionary = {
                    "manga" : i.manga,
                    "manga_id" : manga_result.id,
                    "chapters" : manga_result.chapters_num,
                    "volumes" : manga_result.volumes_num,
                    "type" : manga_result.cast_type,
                    #"score" : score_result.total_score,
                    #"members" : score_result.total,
                    "synopsis" : manga_result.synopsis[:400] + "...",
                    "status" : i.status,
                    "chapters_read" : i.chapters_num,
                    "volumes_read" : i.volumes_num,
                    "reread" : i.reread,
                }
                listing.append(dictionary)
            return listing

    @try_except
    @login_required
    def delete_list():
        manga = request.form['del_list_manga']
        result = Manga_List.query.filter_by(manga=manga, username=current_user.username).delete()
        db.session.commit()

    @login_required
    def suggested_manga():
        manga_list = User_Score_Manga.query.filter_by(username=current_user.username).order_by(User_Score_Manga.score.desc()).limit(3).all()
        all_manga=Manga.query.all()
        result=[]
        count=0
        for i in manga_list:
            manga=Manga.query.filter_by(name_eng=i.manga_name).first()
            genres_manga=manga.genres.rsplit(',')
            for mangas in all_manga:
                c=0
                for m in manga_list:
                    mp=Manga.query.filter_by(name_eng=m.manga_name).first()
                    if mangas.name_eng == mp.name_eng:
                        c=1
                if c==1:
                    continue
                count=0
                genres_mangas=mangas.genres.rsplit(',')
                for genre1 in genres_manga:
                    for genre2 in genres_mangas:
                        if genre2==genre1:
                            count+=1
                if count>3:
                    result.append(mangas)
        result.sort(key=lambda x : x.rank )
        
        return result[:3]

class User_Score_Manga(db.Model):
    __tablename__ = 'user_score_manga'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    manga_name = db.Column(db.String)
    score = db.Column(db.Integer)
    manga_id = db.Column(db.Integer)


class Score_Manga(db.Model):
    __tablename__ = 'score_manga'
    id = db.Column(db.Integer, primary_key=True)
    manga_id = db.Column(db.Integer)
    manga_name = db.Column(db.String)
    score_1 = db.Column(db.Integer, default=0)
    score_2 = db.Column(db.Integer, default=0)
    score_3 = db.Column(db.Integer, default=0)
    score_4 = db.Column(db.Integer, default=0)
    score_5 = db.Column(db.Integer, default=0)
    score_6 = db.Column(db.Integer, default=0)
    score_7 = db.Column(db.Integer, default=0)
    score_8 = db.Column(db.Integer, default=0)
    score_9 = db.Column(db.Integer, default=0)
    score_10 = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Float, default=0)

    @try_except
    @login_required
    def update_score():
        user = current_user.username
        score = int(request.form['score'])
        manga_name = request.form['manga_name']
        result = User_Score_Manga.query.filter_by(username=user, manga_name=manga_name).first()
        #print(result)
        final = Score_Manga.query.filter_by(manga_name=manga_name).first()
        if result:
            temp = result.score
            result.score = score
            total = (final.total_score*final.total - temp + score)/final.total
            if temp==1:
                final.score_1-=1
            elif temp==2:
                final.score_2-=1
            elif temp==3:
                final.score_3-=1
            elif temp==4:
                final.score_4-=1
            elif temp==5:
                final.score_5-=1
            elif temp==6:
                final.score_6-=1
            elif temp==7:
                final.score_7-=1
            elif temp==8:
                final.score_8-=1
            elif temp==9:
                final.score_9-=1
            elif temp==10:
                final.score_10-=1


            if score==1:
                final.score_1+=1
            elif score==2:
                final.score_2+=1
            elif score==3:
                final.score_3+=1
            elif score==4:
                final.score_4+=1
            elif score==5:
                final.score_5+=1
            elif score==6:
                final.score_6+=1
            elif score==7:
                final.score_7+=1
            elif score==8:
                final.score_8+=1
            elif score==9:
                final.score_9+=1
            elif score==10:
                final.score_10+=1

            final.total_score = total
            db.session.merge(result)
            db.session.merge(final)
            db.session.commit()
        else:
            if score==1:
                final.score_1+=1
            elif score==2:
                final.score_2+=1
            elif score==3:
                final.score_3+=1
            elif score==4:
                final.score_4+=1
            elif score==5:
                final.score_5+=1
            elif score==6:
                final.score_6+=1
            elif score==7:
                final.score_7+=1
            elif score==8:
                final.score_8+=1
            elif score==9:
                final.score_9+=1
            elif score==10:
                final.score_10+=1
            final.total+=1
            final.total_score = (final.total_score+score)/final.total 
            manga_id = Manga.query.filter_by(name_eng=manga_name).first().id
            entry = User_Score_Manga(username=user,manga_name=manga_name,score=score,manga_id=manga_id)
            db.session.add(entry)
            db.session.merge(final)
            db.session.commit()
        Manga.update_rank()

    def best(username):
        lis=User_Score_Manga.query.filter_by(username=username).order_by(User_Score_Manga.score.desc()).limit(6).all()
        ans=[]
        for i in lis:
            dic={
            'name' :i.manga_name,
            "id" : i.manga_id,
            "score" : i.score,
            }
            ans.append(dic)
        return ans
            
class Characters_Manga(db.Model):
    __tablename__ = 'characters_manga'
    id = db.Column(db.Integer, primary_key=True)
    name_manga = db.Column(db.String)
    url_char = db.Column(db.String)
    name_char = db.Column(db.String)
    name_jap = db.Column(db.String)
    role = db.Column(db.String)
    data = db.Column(db.String)
    nick = db.Column(db.String)
    manga_id = db.Column(db.Integer,db.ForeignKey('manga.id' , ondelete='CASCADE'))

    def get_charac(num):
        result = Characters_Manga.query.filter_by(id=num).first()
        result_2 = Characters_Manga.query.filter_by(name_char=result.name_char).all()
        #anime = Anime.query.filter_by(name_eng=result.name_anime).first().id
        anime_name=[]
        for res in result_2:
            manga = Manga.query.filter_by(name_eng=res.name_manga).first().id
            dicta={
            'name' : res.name_manga,
            'id' : manga,
            'role' : res.role,
            }
            anime_name.append(dicta)

        data = {
            "mangaography" : anime_name,
            "name_char" : result.name_char,
            "name_jap" : result.name_jap,
            "data" : result.data,
            "nick" : result.nick,
        }
        return data


class Recommendation(db.Model):
    __tablename__="recommendation"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    anime = db.Column(db.String)
    recommend_anime = db.Column(db.String)
    reason = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    #user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    #anime_id = db.Column(db.Integer,db.ForeignKey('anime.id'))

    @try_except
    @login_required
    def add_recommendation():
        username = current_user.username
        anime=request.form['anime_recommend']
        recommend_anime = request.form['recommend_anime']
        #anime_id = Anime.query.filter_by(name_eng=anime).first().id
        result = Recommendation.query.filter_by(username=username, anime=anime).first()
        #anime =  Anime.query.filter_by(name_eng=anime).first()
        reason = request.form['reason']
        create_time = datetime.now()
        last_modified = create_time

        if result:
            result.reason = reason
            result.last_modified= datetime.now()
            #print (result)
            db.session.merge(result)
            db.session.commit()
        else:
            entry = Recommendation(anime=anime,username=username,recommend_anime=recommend_anime,reason=reason,create_time=create_time,last_modified=last_modified)
            db.session.add(entry)
            db.session.commit()

    @try_except
    @login_required
    def edit_recommend():
        username = current_user.username
        anime=request.form['anime_recommend']
        recommend_anime = request.form['edit_recommend_anime']
        reason = request.form['edit_reason']
        last_modified = datetime.now()
        result = Recommendation.query.filter_by(username=username, anime=anime).first()
        result.recommend_anime = recommend_anime
        result.reason = reason
        result.last_modified = last_modified
        db.session.merge(result)
        db.session.commit()

    @try_except
    @login_required
    def delete_recommend(num):
        #print("hello")
        user = current_user.username
        #print("hello")
        result = Anime.query.filter_by(id=num).first()
        #print("hello")
        check_box = request.form.getlist('delete_recommend')[0]
        if (check_box == "on"):
            #print (user)
            #print(result)
            #print("hello")
            query = Recommendation.query.filter_by(username=user, anime=result.name_eng).delete()
            db.session.commit()
            #print(query)

    def get_recommend(anime):
        result = Recommendation.query.filter_by(anime=anime).all()
        details_recommend = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            recommend_id = Anime.query.filter_by(name_eng=entry.recommend_anime).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary_recommend = {
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "recommend_anime" : entry.recommend_anime,
                "elapsed" : elapsed,
                "unit" : unit,
                "recommend_id" : recommend_id,
                #"id" : entry.recommendation.id
            }
            #print(entry.recommendation.id)
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        return details_recommend
    def get_recommend_user(username):
        result = Recommendation.query.filter_by(username=username).all()
        details_recommend = []
        for entry in result:
            anime_id=Anime.query.filter_by(name_eng=entry.anime).first().id
            recommend_id=Anime.query.filter_by(name_eng=entry.recommend_anime).first().id
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary_recommend = {
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "recommend_anime" : entry.recommend_anime,
                "elapsed" : elapsed,
                "unit" : unit,
                "anime" : entry.anime,
                "anime_id": anime_id,
                "recommend_id" :recommend_id,
                #"id" : entry.recommendation.id
            }
            #print(entry.recommendation.id)
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        return details_recommend

    def get_recommend_main():
        result = Recommendation.query.order_by(Recommendation.last_modified.desc()).limit(10).all()
        details_recommend = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            anime_id = Anime.query.filter_by(name_eng=entry.anime).first().id
            recommended_anime_id = Anime.query.filter_by(name_eng=entry.recommend_anime).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary_recommend = {
                "anime_id" : anime_id,
                "recommend_anime_id" : recommended_anime_id,
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "anime" : entry.anime,
                "recommend_anime" : entry.recommend_anime,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        #print("hello")
        #print(details_recommend)
        if len(details_recommend) > 6:
            return details_recommend[:6]
        else:
            return details_recommend


class Recommendation_Manga(db.Model):
    __tablename__="recommendation_manga"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    manga = db.Column(db.String)
    recommended_manga = db.Column(db.String)
    reason = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    #anime_id = db.Column(db.Integer,db.ForeignKey('anime.id'))

    @try_except
    @login_required
    def add_recommendation():
        username = current_user.username
        manga=request.form['manga_recommend']
        recommended_manga = request.form['recommended_manga']
        #anime_id = Anime.query.filter_by(name_eng=anime).first().id
        result = Recommendation_Manga.query.filter_by(username=username, manga=manga).first()
        #anime =  Anime.query.filter_by(name_eng=anime).first()
        reason = request.form['reason']
        create_time = datetime.now()
        last_modified = create_time

        if result:
            result.recommended_manga=recommended_manga
            result.reason = reason
            result.last_modified= datetime.now()
            #print (result)
            db.session.merge(result)
            db.session.commit()
        else:
            entry = Recommendation_Manga(manga=manga,username=username,recommended_manga=recommended_manga,reason=reason,create_time=create_time,last_modified=last_modified)
            db.session.add(entry)
            db.session.commit()


    @try_except
    @login_required
    def edit_recommend():
        username = current_user.username
        manga=request.form['manga_recommend']
        recommended_manga = request.form['edit_recommended_manga']
        reason = request.form['edit_reason']
        last_modified = datetime.now()
        result = Recommendation_Manga.query.filter_by(username=username, manga=manga).first()
        result.recommended_manga= recommended_manga
        result.reason = reason
        result.last_modified = last_modified
        db.session.merge(result)
        db.session.commit()

    @try_except
    @login_required
    def delete_recommend(num):
        user = current_user.username
        result = Manga.query.filter_by(id=num).first()
        check_box = request.form.getlist('delete_recommend')[0]
        if (check_box == "on"):
            #print (user)
            #print(result)
            query = Recommendation_Manga.query.filter_by(username=user, manga=result.name_eng).delete()
            db.session.commit()
            #print(query)

    def get_recommend(manga):
        result = Recommendation_Manga.query.filter_by(manga=manga).all()
        details_recommend = []
        for entry in result:
            manga_id = Manga.query.filter_by(name_eng=entry.recommended_manga).first().id
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary_recommend = {
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "recommended_manga" : entry.recommended_manga,
                "elapsed" : elapsed,
                "unit" : unit,
                "manga_id" : manga_id,
                #"id" : entry.recommendation.id
            }
            
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        return details_recommend

    def get_recommend_user(username):
        result = Recommendation_Manga.query.filter_by(username=username).order_by(Recommendation_Manga.last_modified.desc()).all()
        details_recommend = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            manga_id = Manga.query.filter_by(name_eng=entry.manga).first().id
            recommended_manga_id = Manga.query.filter_by(name_eng=entry.recommended_manga).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, mangaunit)
            dictionary_recommend = {
                "manga_id" : manga_id,
                "recommended_manga_id" : recommended_manga_id,
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "manga" : entry.manga,
                "recommended_manga" : entry.recommended_manga,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        #print("hello")
        return details_recommend



    def get_recommend_main():
        result = Recommendation_Manga.query.order_by(Recommendation_Manga.last_modified.desc()).limit(10).all()
        details_recommend = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            manga_id = Manga.query.filter_by(name_eng=entry.manga).first().id
            recommended_manga_id = Manga.query.filter_by(name_eng=entry.recommended_manga).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, mangaunit)
            dictionary_recommend = {
                "manga_id" : manga_id,
                "recommended_manga_id" : recommended_manga_id,
                "username" : entry.username,
                "reason" : entry.reason,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "manga" : entry.manga,
                "recommended_manga" : entry.recommended_manga,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details_recommend.append(dictionary_recommend)
            #print(details_recommend)
        #print("hello")
        #print(details_recommend)
        if len(details_recommend) > 6:
            return details_recommend[:6]
        else:
            return details_recommend

class Review(db.Model):
    __tablename__="review"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    anime = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    #user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    
    @try_except
    @login_required
    def add_review():
        username = current_user.username
        anime = request.form['anime_review']
        result = Review.query.filter_by(username=username, anime=anime).first()
        title = request.form['review_title']
        content = request.form['review_content']
        #create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_time = datetime.now()
        last_modified = create_time
        print(create_time)

        if result:
            result.title = title
            result.content=content
            #result.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result.last_modified = datetime.now()
            db.session.merge(result)
            db.session.commit()
        else:
            entry = Review(username=username,anime=anime,title=title,content=content,create_time=create_time,last_modified=last_modified )
            #entry = Review(username=username,anime=anime,title=title,content=content)
            db.session.add(entry)
            db.session.commit()

    @try_except
    @login_required
    def edit_review():
        username = current_user.username
        anime = request.form['edit_anime_review']
        title = request.form['edit_review_title']
        content = request.form['edit_review_content']
        #last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_modified = datetime.now()
        result = Review.query.filter_by(username=username, anime=anime).first()
        result.title = title
        result.content = content
        result.last_modified = last_modified
        db.session.merge(result)
        db.session.commit()

    @try_except
    @login_required
    def delete_review(num):
        user = current_user.username
        result = Anime.query.filter_by(id=num).first()
        check_box = request.form.getlist('delete_review')[0]
        if (check_box == "on"):
            #print (user)
            #print(result)
            query = Review.query.filter_by(username=user, anime=result.name_eng).delete()
            db.session.commit()

    def get_review(anime):
        result = Review.query.filter_by(anime=anime).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "title" : entry.title,
                "content" : entry.content,
                "anime" : entry.anime,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details.append(dictionary)
        #print(details)
        return details

    def get_review_user(username):
        result = Review.query.filter_by(username=username).order_by(Review.last_modified.desc()).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            anime_id = Anime.query.filter_by(name_eng=entry.anime).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "anime_id" : anime_id,
                "title" : entry.title,
                "content" : entry.content,
                "anime" : entry.anime,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details.append(dictionary)
        #print(details)
        return details



    def get_review_main():
        result = Review.query.order_by(Review.last_modified.desc()).limit(10).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            anime_id = Anime.query.filter_by(name_eng=entry.anime).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "anime_id" : anime_id,
                "title" : entry.title,
                "content" : entry.content,
                "anime" : entry.anime,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details.append(dictionary)
        #print(details)
        if len(details) > 6:
            return details[:6]
        else:
            return details

class Review_Manga(db.Model):
    __tablename__="review_manga"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    manga = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    
    @try_except
    @login_required
    def add_review():
        username = current_user.username
        manga = request.form['manga_review']
        result = Review_Manga.query.filter_by(username=username, manga=manga).first()
        title = request.form['review_title']
        content = request.form['review_content']
        #create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_time = datetime.now()
        last_modified = create_time
        #print(create_time)

        if result:
            result.title = title
            result.content=content
            #result.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result.last_modified = datetime.now()
            db.session.merge(result)
            db.session.commit()
        else:
            entry = Review_Manga(username=username,manga=manga,title=title,content=content,create_time=create_time,last_modified=last_modified , manga_review_user=current_user)
            #entry = Review(username=username,anime=anime,title=title,content=content)
            db.session.add(entry)
            db.session.commit()

    @try_except
    @login_required
    def edit_review():
        username = current_user.username
        manga = request.form['edit_manga_review']
        title = request.form['edit_review_title']
        content = request.form['edit_review_content']
        #last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_modified = datetime.now()
        result = Review_Manga.query.filter_by(username=username, manga=manga).first()
        result.title = title
        result.content = content
        result.last_modified = last_modified
        db.session.merge(result)
        db.session.commit()

    @try_except
    @login_required
    def delete_review(num):
        user = current_user.username
        result = Manga.query.filter_by(id=num).first()
        check_box = request.form.getlist('delete_review')[0]
        if (check_box == "on"):
            #print (user)
            #print(result)
            query = Review_Manga.query.filter_by(username=user, manga=result.name_eng).delete()
            db.session.commit()
    
    def get_review(manga):
        result = Review_Manga.query.filter_by(manga=manga).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "title" : entry.title,
                "content" : entry.content,
                "manga" : entry.manga,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            #print("dict = "+ dictionary )
            details.append(dictionary)
        #print(details)
        return details

    def get_review_user(username):
        result = Review_Manga.query.order_by(Review_Manga.last_modified.desc()).limit(10).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            manga_id = Manga.query.filter_by(name_eng=entry.manga).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "manga_id" : manga_id,
                "title" : entry.title,
                "content" : entry.content,
                "manga" : entry.manga,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details.append(dictionary)
        #print(details)
        return details


    def get_review_main():
        result = Review_Manga.query.order_by(Review_Manga.last_modified.desc()).limit(10).all()
        details = []
        for entry in result:
            current = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            modified = datetime.strptime(entry.last_modified.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            elapsed = current - modified
            manga_id = Manga.query.filter_by(name_eng=entry.manga).first().id
            #print (timedelta(elapsed))
            if elapsed.days > 0:
                elapsed = elapsed.days
                unit = "day"
            else: 
                if floor(elapsed.seconds/3600) > 0:
                    elapsed = floor(elapsed.seconds/3600)
                    unit = "hour"
                elif floor(elapsed.seconds/60) > 0:
                    elapsed = floor(elapsed.seconds/60)
                    unit = "minute"
                else:
                    elapsed = elapsed.seconds
                    unit = "second"
            #print(elapsed, unit)
            dictionary = {
                "username" : entry.username,
                "manga_id" : manga_id,
                "title" : entry.title,
                "content" : entry.content,
                "manga" : entry.manga,
                "create_time" : entry.create_time,
                "last_modified" : entry.last_modified,
                "elapsed" : elapsed,
                "unit" : unit
            }
            details.append(dictionary)
        #print(details)
        if len(details) > 6:
            return details[:6]
        else:
            return details

db.create_all()

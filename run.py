from flask import Flask , flash, render_template , request , url_for, redirect , abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeSerializer, SignatureExpired, BadSignature
from data.model import *
#from data.model import *
from flask_uploads import UploadSet, configure_uploads, IMAGES
from passlib.hash import sha256_crypt
from flask_mail import Mail,Message

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
UPLOAD_FOLDER = 'static/profilepics'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data/anime.db'
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
configure_uploads(app, photos)

mail = Mail(app)

serializer = URLSafeSerializer(app.secret_key) 

def try_except(func):
	def wrapper(*kwargs):
		try:
			func(*kwargs)
		except:
			pass
	return wrapper

@login_required
def logout():
    logout_user()
    #print('Logged Out!')


@app.route("/", methods=['GET','POST'])
def home():
	top_anime = Anime.top_rank()
	top_manga = Manga.top_rank()
	recent_review=Review.get_review_main()
	recent_recommend=Recommendation.get_recommend_main()
	recent_review_manga=Review_Manga.get_review_main()
	recent_recommend_manga=Recommendation_Manga.get_recommend_main()
	#print(recent_recommend_manga)
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['pwd']

		user = User.query.filter_by(username=username).first()

		if not user:
			#print('User not found!!')
			error="User not found!!"
			flash(error)
			#return render_template("registration.html")
			return redirect(url_for('off'))

		else:
			#print(request.form.getlist('remember'))
			pwd = user.password
			status = sha256_crypt.verify(password,pwd)
			if not status:
				#print("Username/Password does not MATCH")
				error = "Username/Password does not MATCH"
				flash(error)
				return redirect(url_for('off'))

			elif user.verified == False:
				print("Email not Verified")
				error="Email not Verified"
				flash(error)	
				return redirect(url_for('off'))
			else:
				if status:
					try:
						if request.form.getlist('remember')[0] == 'on':
							login_user(user, remember=True)
							#print("remembered")
					except:
						login_user(user, remember=False)
						#print("forgot")
					flash('You are logged in !!')
	return render_template('st.html',top_anime=top_anime,top_manga=top_manga,recent_review_manga=recent_review_manga,num_review_manga=len(recent_review_manga),recent_recommend_manga=recent_recommend_manga,num_recommend_manga=len(recent_recommend_manga),recent_review=recent_review,num_review=len(recent_review),recent_recommend=recent_recommend,num_recommend=len(recent_recommend))


@app.route("/searchresults", methods=['POST'])
def searchres():
	if request.method == 'POST':
		info=[]
		name_eng=request.form['Anime']
		#print(name_eng)
		result = Anime.query.filter(Anime.name_eng.like('%'+name_eng+'%')).all()
		#print (result)
		for i in result:
			query = Score_Anime.query.filter_by(anime_name=i.name_eng).first()
			score = query.total_score
			member = query.total
			dictionary = {
			"name" : i.name_eng,
			"type" : i.cast_type,
			"id" : i.id,
			"synopsis" : i.synopsis[:400]+"...",
			"episodes_num" : i.episodes_num,
			"score" : score ,
			"member" : member,
			}
			info.append(dictionary)
		return render_template("SearchResult.html", anime=info)


@app.route("/mangasearchresults", methods=['POST'])
def mansearchres():
	if request.method == 'POST':
		info=[]
		name_eng=request.form['Manga']
		#print(name_eng)
		result = Manga.query.filter(Anime.name_eng.like('%'+name_eng+'%')).all()
		#print (result)
		for i in result:
			query = Score_Manga.query.filter_by(manga_name=i.name_eng).first()
			score = query.total_score
			member = query.total
			dictionary = {
			"manga_id" : i.id,
			"name" : i.name_eng,
			"type" : i.cast_type,
			"synopsis" : i.synopsis[:400]+"...",
			"chapters_num" : i.chapters_num,
			"volumes_num" : i.volumes_num,
			"score" : score ,
			"member" : member,
			}
			info.append(dictionary)
		return render_template("MangaSearchResults.html", manga=info)




@app.route("/searchanime", methods=['GET','POST'])
def search():
	return render_template("animesearch.html")

@app.route("/topanime",methods=['GET','POST'])
def register():
	if request.method=='POST':
		name=request.form['name']
		username=request.form['username']
		email=request.form['email']
		password=request.form['password']
		repassword=request.form['repassword']
		#print(password,repassword)

		if search_user(username):
			flash("Username already Exists")
			return redirect(url_for('off'))

		if search_email(email):
			flash("Email already Exists")
			return redirect(url_for('off'))

		if password != repassword:
			flash("Passwords do not MATCH")
			return redirect(url_for('off'))

		if not search_user(username) and password==repassword:
			token = serializer.dumps(email, salt="email-confirmation")
			#print(token)
			msg = Message('Email Verification', sender='alokkar1711@gmail.com',recipients=[email])
			link = url_for('confirm_email', token=token,_external=True)
			msg.body = "Click this Link {} to verify your Account".format(link)
			mail.send(msg)
			User.create_user(name,username,email,password,token)
			flash("Successfully Registered")
			return redirect(url_for('home'))
	info=[]
	result = Anime.query.order_by(Anime.rank).all()
	#print (result)
	for i in result:
		query = Score_Anime.query.filter_by(anime_name=i.name_eng).first()
		score = query.total_score
		member = query.total
		dictionary = {
		"name" : i.name_eng,
		"type" : i.cast_type,
		"synopsis" : i.synopsis[:400]+"...",
		"episodes_num" : i.episodes_num,
		"score" : score ,
		"member" : member,
		"id" : i.id,
		}
		info.append(dictionary)
	return render_template('topanime.html' , anime=info)


@app.route("/topmanga",methods=['GET','POST'])
def topmanga():
	info=[]
	result = Manga.query.order_by(Manga.rank).all()
	#print (result)
	for i in result:
		query = Score_Manga.query.filter_by(manga_name=i.name_eng).first()
		score = query.total_score
		member = query.total
		dictionary = {
		"name" : i.name_eng,
		"type" : i.cast_type,
		"synopsis" : i.synopsis[:400]+"...",
		"chapters_num" : i.chapters_num,
		"volumes_num" : i.volumes_num,
		"score" : score ,
		"member" : member,
		"id" : i.id,
		}
		info.append(dictionary)
	return render_template('topmanga.html' , manga=info)





@app.route("/confirm_email/<token>")
def confirm_email(token):
	try:
		email = serializer.loads(token,salt="email-confirmation")
		user = User.query.filter_by(email=email).first()
		if user:
			user.verified = True
			db.session.merge(user)
			db.session.commit()
		return "User Successfully Verified!!"

	except SignatureExpired:
		return "<h1>The token is Expired!</h1>"
	except BadSignature:
		return "<h1>The token is Invalid!</h1>"

@app.route("/userprofile/<username>", methods=['GET','POST'])
def userprofile(username):
	Review.edit_review()
	Review_Manga.edit_review()
	result = User.query.filter_by(username=username).first()
	reviews=Review.get_review_user(username=username)
	reviews_manga=Review_Manga.get_review_user(username)
	recommends=Recommendation.get_recommend_user(username)
	recommends_manga=Recommendation_Manga.get_recommend_user(username)
	dictionary=Anime_List.get_anime_user(username)
	dictionary_manga=Manga_List.get_manga_user(username)
	best_manga_score=Score_Manga.best(username)
	best_anime_score=Score_Anime.best(username)
	suggested_anime = Anime_List.suggested_anime()
	suggested_manga = Manga_List.suggested_manga()
	User.change_name()
	User.change_bio()
	User.change_email()
	User.change_gender()
	User.change_password()
	User.upload()
	return render_template("userprofile.html",username=username,suggested_manga=suggested_manga,suggested_anime=suggested_anime,best_anime_score=best_anime_score,best_manga_score=best_manga_score,bio=result.bio,img_present=result.profilepic,dict=dictionary,dict_manga=dictionary_manga,reviews=reviews,reviews_num=len(reviews),dict_recommend=recommends,recommend_num=len(recommends),reviews_manga=reviews_manga , reviews_manga_num=len(reviews_manga),dict_recommend_manga=recommends_manga,recommend_manga_num=len(recommends_manga))

@app.route("/userprofile/<username>/anime_list", methods=['GET','POST'])
def animelist(username):
	Anime_List.delete_list()
	Anime_List.add_anime()
	dict_list=Anime_List.user_list(username)
	return render_template('animelist.html',username=username,dict_list=dict_list)

@app.route("/userprofile/<username>/manga_list", methods=['GET','POST'])
def mangalist(username):
	Manga_List.delete_list()
	Manga_List.add_manga()
	dict_list=Manga_List.user_list(username)
	return render_template('mangalist.html',username=username, dict_list=dict_list)


@app.route("/registration", methods=['GET','POST'])
def off():
	if request.method == 'POST':
		logout()
	return render_template("registration.html")
@app.route("/anime")
@app.route("/anime/id<num>", methods=['GET','POST'])
def anime(num=1):
	result = Anime.query.filter_by(id=num).first()
	if not result:
		abort(404)
	score=Score_Anime.query.filter_by(anime_id=num).first()
	Score_Anime.update_score()
	dictionary = {
			"rank" : result.rank,
			"score" : score.total_score,
			"name_eng" : result.name_eng,
			"synonyms" : result.synonyms,
			"name_jap" : result.name_jap,
			"cast_type" : result.cast_type,
			"episodes_num" : result.episodes_num,
			"status" : result.status,
			"aired" : result.aired,
			"premiere" : result.premiere,
			"broadcast" : result.broadcast,
			"producers" : result.producers,
			"licensors" : result.licensors,
			"studios" : result.studios,
			"sources" : result.sources,
			"genres" : result.genres,
			"duration" : result.duration,
			"rating" : result.rating,
			"synopsis" : result.synopsis,
			"start_theme" : result.start_theme,
			"end_theme" : result.end_theme
			}
	charac = []
	for i in result.characters:
		dict_char = {
			"name" : i.name_char,
			"role" : i.role,
			"actor" : i.name_actor,
			"language" : i.nationality,
			"id" : i.id,
		}
		charac.append(dict_char)


	score_stats=[]
	score_stats.append(score.total/100)
	score_stats.append(score.score_1)
	score_stats.append(score.score_2)
	score_stats.append(score.score_3)
	score_stats.append(score.score_4)
	score_stats.append(score.score_5)
	score_stats.append(score.score_6)
	score_stats.append(score.score_7)
	score_stats.append(score.score_8)
	score_stats.append(score.score_9)
	score_stats.append(score.score_10)

	#print(charac)
	Animes=Anime.query.all()
	Anime_List.add_anime()
	Review.add_review()
	Review.edit_review()
	Review.delete_review(num)
	Recommendation.add_recommendation()
	Recommendation.edit_recommend()
	Recommendation.delete_recommend(num)
	reviews = Review.get_review(result.name_eng)
	dictionary_anime=Anime_List.get_anime(result.name_eng)
	dictionary_recommend = Recommendation.get_recommend(result.name_eng)
	#print (dictionary_recommend)
	return render_template("animepage.html", animes=Animes ,dict=dictionary,num=num,dict_anime=dictionary_anime,reviews=reviews,reviews_num=len(reviews),characters=charac, characters_num=len(charac), dict_recommend=dictionary_recommend,recommend_num=len(dictionary_recommend), score_stats=score_stats)

@app.route("/char")
@app.route("/char/id<num>", methods=['GET','POST'])
def chars(num=1):
	charac_data=Characters.get_charac(num)
	#print (charac_data)
	return render_template("character.html",charac_data=charac_data)

@app.route("/mangachar")
@app.route("/mangachar/id<num>", methods=['GET','POST'])
def mangachars(num=1):
	charac_data=Characters_Manga.get_charac(num)
	#print (charac_data)
	return render_template("mangachar.html",charac_data=charac_data)
	
@app.route("/manga/id<num>" , methods=['GET' , 'POST' ] )
def manga(num):
	result = Manga.query.filter_by(id=num).first()

	score=Score_Manga.query.filter_by(manga_id=num).first()
	Score_Manga.update_score()

	dictionary = {
			"rank" : result.rank,
			"score" : score.total_score,
			"name_eng" : result.name_eng,
			"altername_eng" : result.altername_eng,
			"synonyms" : result.synonyms,
			"name_jap" : result.name_jap,
			"cast_type" : result.cast_type,
			"volumes_num" : result.volumes_num,
			"chapters_num" : result.chapters_num,
			"status" : result.status,
			"published" : result.published,
			"genres" : result.genres,
			"authors" : result.authors,
			"serialization" : result.serialization,
			"synopsis" : result.synopsis,
			}
	charac = []
	for i in result.characters:
		dict_char = {
			"name" : i.name_char,
			"role" : i.role,
			"id" : i.id,
		}
		charac.append(dict_char)

	#print(dictionary)
	
	score_stats=[]
	score_stats.append(score.total/100)
	score_stats.append(score.score_1)
	score_stats.append(score.score_2)
	score_stats.append(score.score_3)
	score_stats.append(score.score_4)
	score_stats.append(score.score_5)
	score_stats.append(score.score_6)
	score_stats.append(score.score_7)
	score_stats.append(score.score_8)
	score_stats.append(score.score_9)
	score_stats.append(score.score_10)

	Mangas=Manga.query.all()
	Manga_List.add_manga()
	Review_Manga.add_review()
	Review_Manga.edit_review()
	Review_Manga.delete_review(num)
	Recommendation_Manga.add_recommendation()
	Recommendation_Manga.edit_recommend()
	Recommendation_Manga.delete_recommend(num)
	reviews = Review_Manga.get_review(result.name_eng)
	dictionary_recommend = Recommendation_Manga.get_recommend(result.name_eng)
	dictionary_manga=Manga_List.get_manga(result.name_eng)
	return render_template("manga.html",dict=dictionary , reviews=reviews,reviews_num=len(reviews) ,dict_recommend=dictionary_recommend,recommend_num=len(dictionary_recommend) ,mangas=Mangas , dict_manga=dictionary_manga , characters=charac , characters_num=len(charac) , score_stats=score_stats)

@app.route("/mangasearch" , methods=['GET' , 'POST' ])
def mangasearch():
	return render_template("mangasearh.html")

@app.route("/admin",methods=['GET' , 'POST'])
def admin():
	# try:
	# 	if(current_user.privilage==False):
	# 		return redirect(url_for('error'))
	# except:
	# 	abort(404)

	Manga.delete_manga()
	User.delete_user()
	Anime.delete_anime()
	Anime.add_anime()
	Manga.add_manga()
	users = User.display_user()
	anime = Anime.display_anime()
	manga = Manga.display_manga()
	#print(manga)
	return render_template("admin.html",users=users,num_user=len(users),anime=anime,num_anime=len(anime),manga=manga,num_manga=len(manga))

@app.route("/forgotpass" ,methods=['GET' , 'POST' ] )
def forgotpass():
	return render_template('forgotpass.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template("error.html") , 404

@login_manager.user_loader
def load_user(session_token):
	return User.query.filter_by(session_token=session_token).first()

def search_user(username):
	return User.query.filter_by(username=username).first()

def search_email(email):
	return User.query.filter_by(email=email).first()	

if __name__ == '__main__':
	app.run(debug=True)
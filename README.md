# OUR_ANIME_LIST FLASK SERVER

# DEVELOPER
	PURU GUPTA

# FEATURES
*** OurAnimeList is an anime and manga networking and cataloging application website based on MyAnimeList. The site provides its users with a list-like system to organize and score anime and manga. It facilitates finding users who share similar tastes and provides a large database on anime and manga. ***

* Login/Registration functionality
* User Profile Management
* Admin Access Control (Updation and Deletion of Data and User Accounts)
* Suggestions based on watched and favourite animes of user
* Anime and Manga Search
* Favourite Anime List can be made by user
* Watched Anime List can be made by user
* Database of anime and manga with description, cover and voice actors
* Top Anime/Manga on the homepage
* Comments can be added with TimeStamp
* Ratings functionality


# Running the Server
* Requirements
    * Flask - pip3 install flask
    * Flask_Login - pip3 install flask-login
    * Flask_Sqlalchemy - pip3 install Flask-SQLAlchemy
    * Flask_Upload - pip3 install Flask-Uploads
    * Flask_Mail - pip3 install Flask-Mail
    * Passlib - pip3 install passlib
    * ItsDangerous - pip3 install itsdangerous
    
* To run the Flask Server:
	* python3 run.py

* To access the Server:
    * Go to 127.0.0.1:5000 in any web browser

# Running the Scripts to Scrape Data
* Requirements
    * Requests - pip3 install requests
    * BeautifulSoup - pip3 install beautifulsoup4

* To run:
    * python3 ./data/{script_name} 
        * script_name = [animescrape.py, characters_scrape.py, chardata_scrape.py, etc. ]

* To initialize the new database:
    * python3 ./data/db_init.py

* To see the scraped data:
    * Open CSV files in the data directory

* To view the database:
    * sqlite3 ./data/anime.db



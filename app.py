"""
each review has:
id (name + _ + artist) (text)
type (EP or LP) (text)
name (text)
artist (text)
genre (text)
rating (int)
cohesiveness (int)
trackQuality (int)
tags (text (tags are separated by ", "))
beginnerFriendly (text)
inShort (text)
introParagraph (text)
summaryParagraph (text)
opinionParagraph (text)
image (link) (text)
spotifyLink (link) (text)
"""

import os

from flask import Flask
from flask_login import LoginManager

from application.db import create_database, insert_album

from application.login import admin_users, login_bp
from application.home import home_bp
from application.reviews import review_bp
from application.rcreviews import remixcomp_bp
from application.posts import post_bp
from application.admin import admin_bp

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(review_bp)
app.register_blueprint(remixcomp_bp)
app.register_blueprint(post_bp)
app.register_blueprint(admin_bp)

app.config['PREFERRED_URL_SCHEME'] = 'https'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return admin_users.get(id)

create_database()
#insert_album("LP", "Aetherborne", "Chime", "Colour bass", 100, 98, 83, "transitions, melodic, intense, worldbuilding", "eeeeh not really", "storytelling... but colour bass", "insert intro paragraph", "insert summary paragraph", "insert opinion paragraph", "https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d8/59/34/d8593476-09d7-ff92-d944-6831d69edf25/cover.jpg/1200x1200bf-60.jpg", "https://open.spotify.com/album/2rFQGr5i9MfovewAZZnxKF?si=5dde9714577d4fd1")
#insert_album("LP", "The Third Kind", "Dyatic", "Dubstep", 98, 96, 86, "heavy, transitions, worldbuilding, instrumentals, dark", "heh nope", "big action, big creatures, big dubstep", "insert intro paragraph", "insert summary paragraph", "insert opinion paragraph", "https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/62/4f/09/624f0906-9999-960c-c64f-077952286dbc/cover.jpg/1200x1200bf-60.jpg", "https://open.spotify.com/album/6B21DQG1ibFp7ULOaEYiqR?si=59f31971bf6a4ff9")
#insert_rc("World of Slime (Remixes)", "SNAILS", 70, "WIP", "https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/3b/02/e9/3b02e9be-ad92-77cc-0c68-3c9c4566b1cd/192641495434_Download.jpg/1200x1200bf-60.jpg", "https://open.spotify.com/album/0a7dntgGLemxG63D4O3uIz?si=131d463ab7a745c3", "World of Slime_SNAILS")
#insert_album("LP", "Led By Ancient Light", "KOAN Sound", "Liquid drum n bass", 97, 100, 90, "atmospheric, worldbuilding", "kind of", "cinematic bass music for the ages", "WIP", "WIP", "WIP", "https://cdns-images.dzcdn.net/images/cover/69ecea800043a3ff6a38ef473bcf3cf8/0x1900-000000-80-0-0.jpg", "https://open.spotify.com/album/7kh3mjpP4qo8wU9b33LGfF?si=778756bf02b640b6") 

if __name__ == "__main__":
    app.run(host='0.0.0.0')

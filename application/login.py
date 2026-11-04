import os

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__, template_folder="templates")

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

admin_users = {
    os.environ["ADMIN_USERNAME"]: User(os.environ["ADMIN_USERNAME"])
}


def authenticate_user(username, password):
    if username == os.environ["ADMIN_USERNAME"] and check_password_hash(os.environ["ADMIN_PWD"], password):
        return True
    else:
        return False
    

@login_bp.route('/login', methods=['GET','POST'])
def login():  # login page
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            user = User(username)  
            login_user(user)

        return redirect(url_for("home.home"))
    else:
        return render_template("login.html")
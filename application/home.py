from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from application.db import insert_album, insert_rc, filtered_albums, sorted_albums, searched_albums, get_random_album, insert_spotlight, insert_list, get_recent_albums, get_latest_posts, get_hof_albums, get_unfinished_reviews

home_bp = Blueprint("home", __name__)

@home_bp.route('/')  # homepage
def home():
    recent_albums = get_recent_albums()
    hof_albums = get_hof_albums()
    latest_posts = get_latest_posts()

    if current_user.is_authenticated:
        to_review = get_unfinished_reviews()
    else:
        to_review = None

    return render_template("home.html", recent_albums=recent_albums, hof_albums=hof_albums, posts=latest_posts, to_review=to_review)

@home_bp.route("/about")
def about():
    return render_template("construction.html")

@home_bp.route('/add-album', methods=['POST'])
def add_album():
    album_type = request.form.get("type")

    if album_type == "LP" or album_type == "EP":
        name = request.form.get("name").replace("?", "%3F")
        artist = request.form.get("artist").replace("?", "%3F")

        insert_album(album_type, name, artist, "WIP", 0, 0, 0, "WIP", "WIP", "WIP", "WIP", "WIP", "https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313", "/", "WIP", "YYYY/MM/DD", "YYYY/MM/DD")
    
    elif album_type == "RC":
        parent_album_name = request.form.get("parent-name")
        name = request.form.get("name")
        artist = request.form.get("artist")

        parent_album_id = (parent_album_name + "_" + artist).replace(" ", "-")
        insert_rc(name, artist, 0, "WIP", "https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313", "/", parent_album_id, "YYYY/MM/DD")
    
    return redirect(url_for("home.home"))


@home_bp.route('/add-post', methods=['POST'])
def add_post():
    title = request.form.get("title")
    post_type = request.form.get("type")

    postid = title.replace(" ", "-")

    if post_type == "list":
        insert_list(postid, title, "WIP", "https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313")
    elif post_type == "spotlight":
        insert_spotlight(postid, title, "WIP", "WIP", "https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313")
    
    return redirect(url_for("home.home"))
    

@home_bp.route('/search', methods=['POST'])
def search_albums():
    search_key = request.form.get("search").upper()

    lps, eps, rcs = searched_albums(search_key)

    return render_template("home.html", lps=lps, eps=eps, rcs=rcs)
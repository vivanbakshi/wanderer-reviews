import urllib.parse
from flask import Blueprint, render_template, request, redirect, abort
from application.db import get_album, update_album, update_tbt, add_track_tbt, delete_album, delete_track, update_track_quality, get_albums, get_random_album
from flask_login import current_user

review_bp = Blueprint("review", __name__, template_folder="templates")

@review_bp.route("/reviews")
def reviews():
    albums = get_albums()

    return render_template("all_reviews.html", albums=albums)


@review_bp.route("/reviews/random-album")
def reviews_random_album():
    album_id = get_random_album("LP")
    return redirect(f"/review/{album_id}")


@review_bp.route('/review/<string:album_id>')  # album review
def review(album_id):
    album_id = album_id.replace("?", "%3F")
    album_to_render, tbt_table, track_ranking, last_track_index = get_album(album_id)
    decoded_attributes = {
        "name": urllib.parse.unquote(album_to_render["name"]),
        "artist": urllib.parse.unquote(album_to_render["artist"])
    }
    if int(album_to_render["rating"]) != 0 or current_user.is_authenticated:
        return render_template("review.html", album=album_to_render, tbt=tbt_table, ranking=track_ranking, lastTrack=last_track_index, decoded_attributes=decoded_attributes)
    else:
        abort(404)

@review_bp.route('/getedit', methods=['GET', 'POST'])  
def getedit():  # getting an album edit from AJAX
    data = request.form.get('data')  # gets the updated data from the AJAX request
    column = request.form.get('column')  # gets the column to update from AJAX request
    album_id = request.form.get('albumId')  # gets the album ID from AJAX request

    # conversion to int for necessary columns
    if column == "rating" or column == "cohesiveness" or column == "trackQuality":
        try:
            data = float(data)
        except ValueError:
            data = 0

    update_album(album_id, data, column)

    return "success"


@review_bp.route('/update-tbt', methods=['GET', 'POST'])
def get_tbt_edit():
    data = request.form.get("data")
    column = request.form.get("column")
    song_id = request.form.get("songId")
    album_id = request.form.get("albumId")

    if column == "rating":
        try:
            data = float(data)
        except ValueError:
            data = 0

    update_tbt(song_id, data, column, album_id)

    return "success"


@review_bp.route('/add-tbt', methods=['GET','POST'])
def add_new_tbt():
    song_id = request.form.get("songId")
    album_id = request.form.get("albumId")

    add_track_tbt(song_id, album_id)

    return "success"


@review_bp.route('/delete-album', methods=['GET','POST'])
def delete_album_route():
    album_id = request.form.get("albumId")

    delete_album(album_id)

    return "success"

@review_bp.route("/update-review-track-quality", methods=["GET", "POST"])
def update_review_track_quality_route():
    album_id = request.form.get("albumId")

    update_track_quality(album_id)

    return "success"


@review_bp.route('/delete-tbt', methods=["GET", "POST"])
def delete_tbt():
    track_id = request.form.get("songId")

    delete_track(track_id)

    return "success"

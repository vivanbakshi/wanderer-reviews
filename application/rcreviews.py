from flask import Blueprint, render_template, request
from application.db import get_rc, add_rc_track, delete_rc, update_rc, update_rc_track, delete_rc_track, update_rc_track_quality, get_rcs

remixcomp_bp = Blueprint("remixcomp", __name__, template_folder="templates")


@remixcomp_bp.route("/rcreviews")
def rc_review_page():
    rcs = get_rcs()

    return render_template("all_rcs.html", rcs=rcs)


@remixcomp_bp.route('/rcreview/<album_id>')
def rc_review(album_id):
    rc_to_render, tracks, admin_tracks, last_track_index = get_rc(album_id)

    return render_template("rcreview.html", album=rc_to_render, tracks=tracks, admin_tracks=admin_tracks, last_track_index=last_track_index)


@remixcomp_bp.route('/add-rc-song', methods=['GET', 'POST'])
def add_rc_song():
    parent_album = request.form.get("albumId")
    index = request.form.get("index")

    add_rc_track("WIP", index, "WIP", 0, parent_album)

    return "success"


@remixcomp_bp.route('/delete-rc', methods=['GET', 'POST'])
def delete_rc_route():
    album_id = request.form.get("albumId")

    delete_rc(album_id)

    return "success"


@remixcomp_bp.route("/update-rc", methods=["GET", "POST"])
def update_rc_route():
    data = request.form.get("data")
    column = request.form.get("column")
    rc_id = request.form.get("albumId")

    # conversion to int for necessary columns
    if column == "avgRating":
        try:
            data = float(data)
        except ValueError:
            data = 0

    update_rc(rc_id, data, column)

    return "success"


@remixcomp_bp.route("/update-rc-track", methods=["GET", "POST"])
def update_rc_track_route():
    data = request.form.get("data")
    column = request.form.get("column")
    track_id = request.form.get("trackId")
    parent_RC = request.form.get("albumId")

    # conversion to int for necessary columns
    if column == "rating":
        try:
            data = float(data)
        except ValueError:
            data = 0

    update_rc_track(track_id, data, column, parent_RC)

    return "success"

@remixcomp_bp.route("/update-rc-track-quality", methods=["GET", "POST"])
def update_rc_track_quality_route():
    album_id = request.form.get("albumId")

    update_rc_track_quality(album_id)

    return "success"

@remixcomp_bp.route("/delete-rc-track", methods=["GET", "POST"])
def delete_rc_track_route():
    track_id = request.form.get("songId")

    delete_rc_track(track_id)

    return "success"
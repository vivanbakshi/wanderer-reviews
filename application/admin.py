from flask import Blueprint, request, render_template
from flask_login import login_required

from application.db import get_stat_by_type, update_album

admin_bp = Blueprint("admin", __name__, template_folder="templates")

@admin_bp.route("/admin-stats/<albumtype>/<stat>")
@login_required
def admin_stat(albumtype, stat):
    albums = get_stat_by_type(albumtype, stat)

    return render_template("adminstats.html", albums=albums, stat=stat)


@admin_bp.route("/admin-stats-edit", methods=['GET', 'POST'])
@login_required
def admin_edit():
    column = request.form.get("column")
    album_id = request.form.get("albumId")
    data = request.form.get("data")

    update_album(album_id, data, column)

    return "success"


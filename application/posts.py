from flask import Blueprint, render_template, request, redirect
from application.db import get_spotlight, insert_list_item, get_list, delete_spotlight, delete_list, edit_list, edit_spotlight, edit_list_item, delete_list_item, get_posts

post_bp = Blueprint("spotlight", __name__, template_folder="templates")

@post_bp.route("/posts")
def posts_page():
    posts = get_posts()

    return render_template("all_posts.html", posts=posts)

@post_bp.route("/posts/<postid>")
def post(postid):
    spotlight_to_render = get_spotlight(postid)
    if not spotlight_to_render:
        list_to_render, listitems = get_list(postid)
        return render_template("list.html", list=list_to_render, listitems=listitems)

    return render_template("spotlight.html", post=spotlight_to_render)


@post_bp.route('/delete-post', methods=['GET', 'POST'])
def delete_post():
    postid = request.form.get("postId")
    post_type = request.form.get("type")

    if post_type == "spotlight":
        delete_spotlight(postid)
    elif post_type == "list":
        delete_list(postid)
    
    return "success"


@post_bp.route('/edit-post', methods=['GET', 'POST'])
def edit_post():
    data = request.form.get("data")
    column = request.form.get("column")
    post_type = request.form.get("type")
    postid = request.form.get("postId")

    if post_type == "spotlight":
        edit_spotlight(data, column, postid)
    elif post_type == "list":
        edit_list(data, column, postid)

    return "success"

@post_bp.route('/add-list-item', methods=['GET', 'POST'])
def add_item():
    parentid = request.form.get("postId")

    insert_list_item("WIP", "WIP", "WIP", "https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313", parentid)

    return "success"

@post_bp.route('/edit-list-item', methods=['GET', 'POST'])
def edit_post_item():
    item_number = request.form.get("itemNumber")
    data = request.form.get("data")
    column = request.form.get("column")
    parent_listid = request.form.get("postId")

    itemid = parent_listid + "_" + str(item_number)

    edit_list_item(data, column, itemid)

    return "success"


@post_bp.route('/delete-list-item', methods=['GET', 'POST'])
def delete_item():
    postid = request.form.get("postId")

    delete_list_item(postid)

    return "success"
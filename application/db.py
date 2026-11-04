import sqlite3
import datetime
from flask_login import login_required

def create_database():  # creates database
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS albums(id TEXT PRIMARY KEY, type TEXT, name TEXT, artist TEXT, genre TEXT, rating INT, cohesiveness INT, trackQuality INT, tags text, beginnerFriendly TEXT, inShort TEXT, introParagraph TEXT, summaryParagraph TEXT, opinionParagraph TEXT, image TEXT, spotifyLink TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS songs(trackid TEXT PRIMARY KEY, number INT, name TEXT, comments TEXT, collabs TEXT, superlative TEXT, rating INT, parentAlbum TEXT, FOREIGN KEY(parentAlbum) REFERENCES albums(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS remixcomps(id TEXT PRIMARY KEY, name TEXT, artist TEXT, avgRating INT, notes TEXT, image TEXT, spotifyLink TEXT, parentAlbum TEXT, FOREIGN KEY(parentAlbum) REFERENCES albums(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS rcsongs(trackid TEXT PRIMARY KEY, number INTEGER, name TEXT, comments TEXT, rating INT, parentRC TEXT, FOREIGN KEY(parentRC) REFERENCES remixcomps(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS spotlights(id TEXT PRIMARY KEY, title TEXT, summary TEXT, content TEXT, dateCreated TEXT, leadImage TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS lists(id TEXT PRIMARY KEY, title TEXT, summary TEXT, dateCreated TEXT, leadImage TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS listitems(id TEXT PRIMARY KEY, number INTEGER, title TEXT, artist TEXT, content TEXT, image TEXT, parentList TEXT, FOREIGN KEY(parentList) REFERENCES lists(id))")
    
    
    connection.commit()
    connection.close()


##################### REVIEW #####################

def get_album(album_id):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM albums WHERE id = ?", (album_id,))
    album_to_render = cursor.fetchone()

    cursor.execute("SELECT * FROM songs WHERE parentAlbum = ? ORDER BY number ASC", (album_id,))
    tbt_table = cursor.fetchall()
    
    cursor.execute("SELECT * FROM songs WHERE parentAlbum = ? ORDER BY rating DESC", (album_id,))
    track_ranking = cursor.fetchall()

    connection.close()

    if len(tbt_table) > 0:
        last_track_index = tbt_table[len(tbt_table) - 1]["number"] + 1
    else:
        last_track_index = 0

    return album_to_render, tbt_table, track_ranking, last_track_index

@login_required
def insert_album(project_type, name, artist, genre, rating, cohesiveness, track_quality, tags, beginner_friendly, intro_paragraph, summary_paragraph, opinion_paragraph, image_href, spotify_link, image_credit, date, release_date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO albums VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{name}_{artist}".replace(" ", "-"), project_type, name, artist, genre, rating, cohesiveness, track_quality, tags, beginner_friendly, intro_paragraph, summary_paragraph, opinion_paragraph, image_href, spotify_link, image_credit, date, release_date))
    except sqlite3.IntegrityError:
        print("album already exists")
    
    connection.commit()
    connection.close()

@login_required
def update_album(unique_id, data, column):
    columns = ["type", "name", "artist", "genre", "rating", "cohesiveness", "trackQuality", "tags", "beginnerFriendly", "introParagraph", "summaryParagraph", "opinionParagraph", "trackByTrack", "image", "spotifyLink", "imageCopyright", "date", "releaseDate"]
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    if column in columns: 
        cursor.execute(f"UPDATE albums SET {column}=? WHERE id=?", (data, unique_id))  # updates specific row with specified data and column
    connection.commit()
    connection.close()

@login_required
def add_track_tbt(song_id, album_id):
    split_song_id = song_id.split("_")
    index = int(split_song_id[len(split_song_id)-1])

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO songs VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (song_id, index, "WIP", "WIP", "WIP", "WIP", 0, album_id))
    except sqlite3.IntegrityError:
        print("song already exists")
    connection.commit()
    connection.close()

@login_required
def update_tbt(song_id, data, column, album_id):
    columns = ['name', 'collabs', 'comments', 'superlative', 'rating']

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    if column in columns:
        cursor.execute(f"UPDATE songs SET {column}=? WHERE (trackid=? OR name=?) AND parentAlbum=?", (data, song_id, song_id, album_id))
        connection.commit()
    connection.close()

@login_required
def update_track_quality(album_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT rating FROM songs WHERE parentAlbum=?", (album_id,))
    tracks = cursor.fetchall()

    total = 0
    for track in tracks:
        total = total + track[0]
    total = total / len(tracks)

    cursor.execute("UPDATE albums SET trackQuality=? WHERE id=?", (total, album_id))
    connection.commit()
    connection.close()

@login_required
def delete_album(album_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM albums WHERE id=?", (album_id,))
    cursor.execute("DELETE FROM songs WHERE parentAlbum=?", (album_id,))
    connection.commit()
    connection.close()

@login_required
def delete_track(track_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM songs WHERE trackid=?", (track_id,))
    connection.commit()
    connection.close()

##################### REMIX COMPS #####################

def get_rc(album_id):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM remixcomps WHERE id=?", (album_id,))
    rc_to_render = cursor.fetchone()

    cursor.execute("SELECT * FROM rcsongs WHERE parentRC=? ORDER BY rating DESC", (album_id,))
    tracks = cursor.fetchall()

    cursor.execute("SELECT * FROM rcsongs WHERE parentRC=? ORDER BY number ASC", (album_id,))
    admin_tracks = cursor.fetchall()

    if len(admin_tracks) > 0:
        last_track_index = admin_tracks[len(admin_tracks) - 1]["number"]
    else:
        last_track_index = 0

    connection.close()

    return rc_to_render, tracks, admin_tracks, last_track_index

@login_required
def insert_rc(name, artist, avg_rating, notes, image_link, spotify_link, parent_album, date):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO remixcomps VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{name}_{artist}".replace(" ", "-"), name, artist, avg_rating, notes, image_link, spotify_link, parent_album, date, "/"))
    except sqlite3.IntegrityError:
        print("album already exists")
    connection.commit()
    connection.close()

@login_required
def update_rc(rc_id, data, column):
    columns = ["avgRating", "notes", "image", "spotifyLink", "date", "imageCopyright"]
    if column in columns:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE remixcomps SET {column}=? WHERE id=?", (data, rc_id))
        connection.commit()
        connection.close()

@login_required
def add_rc_track(name, index, comments, rating, parent_album_id):
    track_id = parent_album_id + "_" + index
    print(name, index, comments, rating, parent_album_id, track_id)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO rcsongs VALUES(?, ?, ?, ?, ?, ?)", (track_id, int(index), name, comments, int(rating), parent_album_id))
    except sqlite3.IntegrityError:
        print("song already exists")
    connection.commit()
    connection.close()

@login_required
def update_rc_track(track_id, data, column, parentRC):
    columns = ["name", "comments", "rating"]
    if column in columns:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE rcsongs SET {column}=? WHERE trackid=? AND parentRC=?", (data, track_id, parentRC))
        connection.commit()
        connection.close()

@login_required
def update_rc_track_quality(album_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT rating FROM rcsongs WHERE parentRC=?", (album_id,))
    tracks = cursor.fetchall()

    total = 0
    for track in tracks:
        total = total + track[0]
    total = total / len(tracks)

    cursor.execute("UPDATE remixcomps SET avgRating=? WHERE id=?", (total, album_id))
    
    connection.commit()
    connection.close()

@login_required
def delete_rc(rc_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM remixcomps WHERE id=?", (rc_id,))
    cursor.execute("DELETE FROM rcsongs WHERE parentRC=?", (rc_id,))
    connection.commit()
    connection.close()

@login_required
def delete_rc_track(track_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM rcsongs WHERE trackid=?", (track_id,))
    connection.commit()
    connection.close()

##################### HOMEPAGE #####################

def get_albums():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, tags, introParagraph, image, date, releaseDate FROM albums WHERE type=? ORDER BY date DESC, rowid DESC", ("LP",))
    lps = cursor.fetchall()
    connection.close()

    return lps


@login_required
def get_unfinished_reviews():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, tags, introParagraph, image, date, releaseDate FROM albums WHERE type=? AND rating=? ORDER BY date DESC, rowid DESC", ("LP", 0))
    albums = cursor.fetchall()

    connection.close()
    return albums

def get_rcs():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, avgRating, notes, image, date FROM remixcomps ORDER BY date DESC, rowid DESC")
    rcs = cursor.fetchall()

    connection.close()
    return rcs


def filtered_albums(filter_key):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, image FROM albums WHERE instr(tags, ?) > 0 AND type=? ORDER BY rating DESC", (filter_key, "LP"))
    lps = cursor.fetchall()

    cursor.execute("SELECT id, name, artist, genre, rating, image FROM albums WHERE instr(tags, ?) > 0 AND type=? ORDER BY rating DESC", (filter_key, "EP"))
    eps = cursor.fetchall()

    connection.close()

    return lps, eps


def sorted_albums(sort_key):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(f"SELECT id, name, artist, genre, rating, image FROM albums WHERE type=? ORDER BY {sort_key} DESC", ("LP",))
    lps = cursor.fetchall()

    cursor.execute(f"SELECT id, name, artist, genre, rating, image FROM albums WHERE type=? ORDER BY {sort_key} DESC", ("EP",))
    eps = cursor.fetchall()

    cursor.execute("SELECT id, name, artist, avgRating, image FROM remixcomps ORDER BY avgRating DESC")
    rcs = cursor.fetchall()

    connection.close()

    return lps, eps, rcs


def searched_albums(search_key):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, image FROM albums WHERE (instr(upper(name), ?) > 0 OR instr(upper(artist), ?) > 0 OR instr(upper(genre), ?) > 0) AND type=? ORDER BY rating DESC", (search_key, search_key, search_key, "LP"))
    lps = cursor.fetchall()

    cursor.execute("SELECT id, name, artist, genre, rating, image FROM albums WHERE (instr(upper(name), ?) > 0 OR instr(upper(artist), ?) > 0 OR instr(upper(genre), ?) > 0) AND type=? ORDER BY rating DESC", (search_key, search_key, search_key, "EP"))
    eps = cursor.fetchall()

    cursor.execute("SELECT id, name, artist, image, avgRating FROM remixcomps WHERE instr(upper(name), ?) > 0 OR instr(upper(artist), ?) > 0 ORDER BY avgRating DESC", (search_key, search_key))
    rcs = cursor.fetchall()

    connection.close()

    return lps, eps, rcs


def get_random_album(album_type):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM albums WHERE type=? AND rating != ? ORDER BY RANDOM() LIMIT 1", (album_type, 0))
    album_id = cursor.fetchone()[0]

    connection.close()

    return album_id

def get_recent_albums():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, tags, introParagraph, image, date FROM albums WHERE type=? AND rating > 0 ORDER BY date DESC, rowid DESC LIMIT 4", ("LP",))
    albums = cursor.fetchall()

    connection.close()
    return albums

def get_latest_posts():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM(SELECT id, title, summary, leadImage, dateCreated FROM spotlights UNION SELECT id, title, summary, leadImage, dateCreated FROM lists) WHERE leadImage != ? ORDER BY dateCreated DESC LIMIT 5", ("https://ik.imagekit.io/thewandererreviews/logo.svg?updatedAt=1738429520313",))
    posts = cursor.fetchall()

    connection.close()
    return posts


def get_hof_albums():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, artist, genre, rating, tags, introParagraph, image, date FROM albums WHERE type=? AND rating >= 87.5 ORDER BY rating DESC LIMIT 4", ("LP",))
    albums = cursor.fetchall()

    connection.close()
    return albums

######################## SPOTLIGHTS #######################


def get_posts():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM(SELECT id, title, summary, leadImage, dateCreated FROM spotlights UNION SELECT id, title, summary, leadImage, dateCreated FROM lists) ORDER BY dateCreated DESC")
    posts = cursor.fetchall()

    connection.close()

    return posts

@login_required
def insert_spotlight(postid, title, summary, content, lead_image):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    date = datetime.date.today()

    try:
        cursor.execute("INSERT INTO spotlights VALUES(?, ?, ?, ?, ?, ?)", (postid, title, summary, content, date, lead_image))
        connection.commit()
    except sqlite3.IntegrityError:
        print("spotlight already exists")

    connection.close()


def get_spotlight(postid):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM spotlights WHERE id = ?", (postid,))
    spotlight = cursor.fetchone()

    connection.close()

    return spotlight

@login_required
def delete_spotlight(postid):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM spotlights WHERE id = ?", (postid,))

    connection.commit()
    connection.close()

@login_required
def edit_spotlight(data, column, postid):
    columns = ["title", "summary", "content", "dateCreated", "leadImage"]
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if column in columns:
        cursor.execute(f"UPDATE spotlights SET {column} = ? WHERE id = ?", (data, postid))
        connection.commit()
    
    connection.close()


########################### LISTS ###########################

@login_required
def insert_list(listid, title, summary, lead_image):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    date = datetime.date.today()

    try:
        cursor.execute("INSERT INTO lists VALUES(?, ?, ?, ?, ?, ?, ?)", (listid, title, summary, date, lead_image, "true", "WIP"))
        connection.commit()
    except sqlite3.IntegrityError:
        print("list already exists")

    connection.close()

@login_required
def insert_list_item(title, artist, content, image, parent_listid):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT number FROM listitems WHERE parentList = ? ORDER BY number DESC LIMIT 1", (parent_listid,))
    previous_number = cursor.fetchone()
    print(previous_number)

    if previous_number:
        number = int(previous_number[0]) + 1
    else:
        number = 1

    itemid = parent_listid + "_" + str(number)

    try:
        cursor.execute("INSERT INTO listitems VALUES(?, ?, ?, ?, ?, ?, ?)", (itemid, number, title, artist, content, image, parent_listid))
        connection.commit()
    except sqlite3.IntegrityError:
        print("list item already exists")

    connection.close()


def get_list(listid):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM lists WHERE id = ?", (listid,))
    list_to_render = cursor.fetchone()

    cursor.execute("SELECT * FROM listitems WHERE parentList = ? ORDER BY number DESC", (listid,))
    listitems = cursor.fetchall()

    connection.close()

    return list_to_render, listitems

@login_required
def delete_list(listid):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM lists WHERE id = ?", (listid,))
    cursor.execute("DELETE FROM listitems WHERE parentList = ?", (listid,))

    connection.commit()
    connection.close()

@login_required
def edit_list(data, column, listid):
    columns = ["title", "summary", "dateCreated", "leadImage", "ordered", "introParagraph"]
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if column in columns:
        cursor.execute(f"UPDATE lists SET {column} = ? WHERE id = ?", (data, listid))
        connection.commit()
    
    connection.close()

@login_required
def edit_list_item(data, column, itemid):
    columns = ["title", "artist", "content", "image"]
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    print(data, column, itemid)

    if column in columns:
        cursor.execute(f"UPDATE listitems SET {column} = ? WHERE id = ?", (data, itemid))
        connection.commit()
    
    connection.close()

@login_required
def delete_list_item(postid):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT number FROM listitems WHERE parentList = ? ORDER BY number DESC LIMIT 1", (postid,))
    number = cursor.fetchone()

    if number:
        itemid = postid + "_" + str(number[0])
        cursor.execute("DELETE FROM listitems WHERE id = ?", (itemid,))
        connection.commit()

    connection.close()


########################### ADMIN ###########################


def get_stat_by_type(album_type, stat):
    stats = ["cohesiveness", "trackQuality", "rating", "date", "tags"]
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stat in stats:
        cursor.execute(f"SELECT id, {stat} FROM albums WHERE type = ? ORDER BY {stat} DESC", (album_type,))
        album_stats = cursor.fetchall()

        connection.close()
        return album_stats
    
    connection.close()

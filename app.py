import os
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from bson import json_util
import json
from datetime import date, datetime
import bcrypt

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'greenlit'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    error = None
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('add_pitch'))
        return 'Invalid Password'
    #     return render_template('login.html', error = error)
    # return 'Invalid Username'
    return render_template('index.html', error = error)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists!'
    return render_template('register.html')

"""
should show session user and list of pitches with option to edit
and maybe to add a profile?
"""

@app.route('/show_pitches', defaults={'sort_field': 'last_modified'})
@app.route('/show_pitches/<sort_field>')
def show_pitches(sort_field):
    pitches = mongo.db.pitches.find().sort(sort_field, pymongo.DESCENDING)
    tags = mongo.db.tags.find()
    users = mongo.db.users.find()
    return render_template("show_pitches.html", pitches=pitches, tags=tags)

@app.route('/show_users')
def show_users():
    return render_template("show_users.html", users=mongo.db.users.find())

@app.route('/add_pitch')
def add_pitch():
    _genres = mongo.db.genres.find()
    genre_list = [genre for genre in _genres]
    _directors = mongo.db.directors.find()
    director_list = [directors for directors in _directors]
    _actors = mongo.db.talent.find()
    actor_list = [actors for actors in _actors]
    _tag_titles = mongo.db.tags.find({"type": "title"},{"title": 1})
    tag_titles_list = [title for title in _tag_titles]
    _tag_locations = mongo.db.tags.find({"type": "loc"},{"location": 1})
    tag_locations_list = [location for location in _tag_locations]
    return render_template('add_pitch.html', genres = genre_list, directors=director_list, actors=actor_list, tag_titles=tag_titles_list, 
    tag_locations=tag_locations_list)


@app.route('/insert_pitch', methods=['POST'])
def insert_pitch():
    created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    last_modified = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    usercoll = mongo.db.users
    username = session['username']
    the_user = usercoll.find_one({'username': username})
    tags = mongo.db.tags
    pitch = mongo.db.pitches
    title = request.form.get('title')
    genre_name = request.form.get('genre_name')
    director_name = request.form.get('director_name')
    actor_name = request.form.get('actor')
    description = request.form.get('discription')
    tag_film1 = request.form.get('film_1')
    tag_film2 = request.form.get('film_2')
    tag_location = request.form.get('location')
    tag_img1 = tags.find_one({'title': tag_film1}, {"img": 1, "_id": 0})
    tag_img2 = tags.find_one({'title': tag_film2}, {"img": 1, "_id": 0})
    loc_img = tags.find_one({'location': tag_location}, {"img": 1, "_id": 0})
    pitch.insert_one({'user_id': the_user['_id'], 'created_at': created_at,
                    'last_modified': last_modified,'title': title,
                    'genre_name': genre_name, 'director_name': director_name,
                    'actor': actor_name, 'description': description,
                    'tag':{'film1':tag_film1,'film2':tag_film2,'location':tag_location},
                    'imgs':{'tag_img1':tag_img1,'tag_img2':tag_img2,'loc_img':loc_img },
                    'is_del':False
                    })
    return redirect(url_for('add_pitch'))


@app.route('/edit_pitch/<pitch_id>')
def edit_pitch(pitch_id):
    _genres = mongo.db.genres.find()
    genre_list = [genre for genre in _genres]
    _directors = mongo.db.directors.find()
    director_list = [directors for directors in _directors]
    _actors = mongo.db.talent.find()
    actor_list = [actors for actors in _actors]
    _tag_titles = mongo.db.tags.find({"type": "title"},{"title": 1})
    tag_titles_list = [title for title in _tag_titles]
    _tag_locations = mongo.db.tags.find({"type": "loc"},{"location": 1})
    tag_locations_list = [location for location in _tag_locations]
    the_pitch = mongo.db.pitches.find_one({"_id": ObjectId(pitch_id)})
    return render_template('edit_pitch.html', 
                            pitch=the_pitch, 
                            genres = genre_list, 
                            directors = director_list, 
                            actors=actor_list, 
                            tag_titles=tag_titles_list, 
                            tag_locations=tag_locations_list)


@app.route('/update_pitch/<pitch_id>', methods=["POST"])
def update_pitch(pitch_id):
    pitches = mongo.db.pitches
    tags = mongo.db.tags
    last_modified = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pitches.update( {'_id': ObjectId(pitch_id)},
    {"$set": {
        'title':request.form.get('title'),
        'genre_name':request.form.get('genre_name'),
        'director_name':request.form.get('director'),
        'actor':request.form.get('actor'),
        'description':request.form.get('description'),
        'tag.film1':request.form.get('tag1'),
        'tag.film2':request.form.get('tag2'),
        'tag.location':request.form.get('location'),
        'imgs.tag_img1':tags.find_one({'title': request.form.get('tag1')}, {"img": 1, "_id": 0}),
        'imgs.tag_img2':tags.find_one({'title': request.form.get('tag2')}, {"img": 1, "_id": 0}),
        'imgs.loc_img':tags.find_one({'location': request.form.get('location')}, {"img": 1, "_id": 0}),
        'last_modified':last_modified,
        'is_del':False
        }
    })
    return redirect(url_for('show_pitches'))

@app.route('/hide_pitch/<pitch_id>', methods=["POST"])
def hide_pitch(pitch_id):
    pitches = mongo.db.pitches
    pitches.update( {'_id': ObjectId(pitch_id)},
    {"$set": {
        'is_del':True
    }})
    return redirect(url_for('show_pitches'))

@app.route('/delete_pitch/<pitch_id>')
def delete_pitch(pitch_id):
    pitches = mongo.db.pitches
    pitches.remove({'_id': ObjectId(pitch_id)})
    flash('Your pitch has been removed from further consideration!')
    return redirect(url_for('show_pitches'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.getenv('PORT'),
            debug=True)
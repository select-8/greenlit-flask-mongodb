import os
from flask import Flask, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
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

@app.route('/add_tag')
def add_tages():
    tags = mongo.db.tags
    tags.insert_one({'title':'Gone With The Wind', 'img':''})
    tags.insert_one({'title':'Scarface', 'img':''})
    tags.insert_one({'title':'Alien', 'img':''})
    tags.insert_one({'title':'The Odd Couple', 'img':''})
    tags.insert_one({'title':'Forest Gump', 'img':''})
    return 'tag in'

# @app.route('/get_tags')
# def get_tags():
#     tag = mongo.db.tags.find()
#     return str(json.dumps({'tags':list(tag)},default=json_util.default)) 

@app.route('/show_pitches')
def show_pitches():
    pitches = mongo.db.pitches.find()
    tags = mongo.db.tags.find()
    return render_template("show_pitches.html", pitches=pitches, tags=tags)

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
        # return render_template('login.html', error = error)
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
    _tags = mongo.db.tags.find()
    tags_list = [tags for tags in _tags]
    return render_template('add_pitch.html', genres = genre_list, directors = director_list, actors=actor_list, tags=tags_list)


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
    # tag_location = request.form.get('location')
    # tag_img1 = tags.find({'title': request.form.get('film_1')}, {"img": 1})
    # tag_img2 = tags.find({'title': tag_film2}, {"img": 1})
    # loc_img = tags.find({'title': tag_location}, {"img": 1})
    # return tag_img1
    pitch.insert_one({'user_id': the_user['_id'], 'created_at': created_at, 
                      'last_modified': last_modified,'title': title,
                      'genre_name': genre_name, 'director_name': director_name,
                      'actor': actor_name, 'description': description, 
                      'tag':{'film1':tag_film1,'film2':tag_film2,'location':tag_location}
    #                   ,
    #                   'imgs':{'tag_img1':tag_img1,'tag_img2':tag_img2,'loc_img':loc_img }
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
    the_pitch = mongo.db.pitches.find_one({"_id": ObjectId(pitch_id)})
    return render_template('edit_pitch.html', pitch=the_pitch, genres = genre_list, directors = director_list, actors=actor_list)

@app.route('/update_pitch/<pitch_id>', methods=["POST"])
def update_pitch(pitch_id):
    pitches = mongo.db.pitches
    last_modified = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pitches.update( {'_id': ObjectId(pitch_id)},
    {"$set": {
        'title':request.form.get('title'),
        'genre_name':request.form.get('genre_name'),
        'director_name':request.form.get('director'),
        'actor':request.form.get('actor'),
        'description':request.form.get('description'),
        'last_modified':last_modified
        }
    })
    return redirect(url_for('show_pitches'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.getenv('PORT'),
            debug=True)
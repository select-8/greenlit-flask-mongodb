import os
import random
import json
import bcrypt
from random import randint
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from bson import json_util
from datetime import date, datetime


app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'greenlit'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

_users = mongo.db.users
users = _users.find()
_pitches = mongo.db.pitches
_genres = mongo.db.genres
_directors = mongo.db.directors
_actors = mongo.db.talent
_tags = mongo.db.tags
tags = _tags.find()
_votes = mongo.db.votes

created_at = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
last_modified = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

@app.route('/')
def index():
    error = None
    username = session.get('username')
    count = _pitches.count({'username' : username})
    return render_template('index.html', count=count)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        login_user = _users.find_one({'username' : request.form['username']})
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('user_pitches'))
        return 'Invalid Password'
    # return render_template('login.html', error = error)
        return 'Invalid Username'
    return render_template('login.html', error = error)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # users = mongo.db.users
        existing_user = _users.find_one({'username' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            _users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists!'
    return render_template('register.html')


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('login'))


@app.route('/user_pitches', defaults={'sort_field': 'last_modified'})
@app.route('/user_pitches/<sort_field>')
def user_pitches(sort_field):
    pitches = _pitches.find().sort(sort_field, pymongo.DESCENDING)
    username = session.get('username')
    status = mongo.db.status.find()
    count = _pitches.count({'username' : username})
    if session.get('logged_in') == True:
        return render_template("user_pitches.html", pitches=pitches, tags=tags, users=users, count=count, statuses=status)
    else:
        return redirect(url_for('all_pitches'))


@app.route('/all_pitches', defaults={'sort_field': 'last_modified'})
@app.route('/all_pitches/<sort_field>')
def all_pitches(sort_field):
    pitches = _pitches.find().sort(sort_field, pymongo.DESCENDING)
    votes = _votes.find_one()
    genres = _genres.find()
    status = mongo.db.status.find()
    return render_template("all_pitches.html", pitches=pitches, tags=tags, votes=votes, genres=genres)


@app.route('/filter_genre', defaults={'gfilter': {'$regex': '.*'}, 'sort_field': 'last_modified'})
@app.route('/filter_genre/<gfilter>/<sort_field>')
def filter_genre(gfilter, sort_field):
    pitch_by_genre = _pitches.find({'genre_name': gfilter}).sort(sort_field, pymongo.DESCENDING)
    count = pitch_by_genre.count()
    if count == 0:
        flash("Currently no entries exist under that genre, maybe you should add one!")
    return render_template("filter_genre.html", pitches_by_genre=pitch_by_genre, count=count)


@app.route('/filter_status', defaults={'sfilter': {'$regex': '.*'}, 'sort_field': 'last_modified'})
@app.route('/filter_status/<sfilter>/<sort_field>')
def filter_status(sfilter, sort_field):
    username = session.get('username')
    pitch_by_status = _pitches.find({'username': username,'is_greenlit': sfilter}).sort(sort_field, pymongo.DESCENDING)
    return render_template("filter_status.html", pitches_by_status=pitch_by_status, username=username)


@app.route('/show_users')
def show_users():
    usercoll = mongo.db.users
    username = session.get('username')
    the_user = usercoll.find_one({'username': username})
    return render_template("show_users.html", user=the_user)


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
    usercoll = mongo.db.users
    # username = session['username']
    username = session.get('username')
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
    pitch.insert_one({'username': the_user['username'], 'created_at': created_at,
                    'last_modified': last_modified,'title': title,
                    'genre_name': genre_name, 'director_name': director_name,
                    'actor': actor_name, 'description': description,
                    'tag':{'film1':tag_film1,'film2':tag_film2,'location':tag_location},
                    'imgs':{'tag_img1':tag_img1,'tag_img2':tag_img2,'loc_img':loc_img },
                    'is_del':False, 'votes':0, 'is_greenlit': '0'
                    })
    # return redirect(url_for('insert_vote'))
    flash('your pitch has been added')
    return redirect(url_for('add_pitch'))
    # find_one_and_update

# @app.route('/insert_vote', methods=["POST", "GET"])
# def insert_vote():
#     lastest_pitch = _pitches.find({},{"_id": 1, 'username': 1}).sort("created_at", -1).limit(1);
#     _votes.insert(lastest_pitch)
#     return redirect(url_for('all_pitches'))


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
    # last_modified = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
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
    return redirect(url_for('user_pitches'))


@app.route('/is_greenlit/<pitch_id>', methods=["GET", "POST"])
def is_greenlit(pitch_id):
    random_is_greenlit = str(randint(0,1))
    bad_actor = _pitches.find_one({'_id':ObjectId(pitch_id)},{'actor': 1, '_id': 0})
    bad_director = _pitches.find_one({'_id':ObjectId(pitch_id)},{'director_name': 1, '_id': 0})
    for ka, va in bad_actor.items():
        for kd, vd in bad_director.items():
            if va == 'Matt Damon':
                _pitches.update( {'_id': ObjectId(pitch_id)},
                {"$set": {'is_greenlit':0}})
                flash('no way lad, not Matt Damon')
            elif va == 'Spike Jones' and vd == 'David O Russell':
                _pitches.update( {'_id': ObjectId(pitch_id)},
                {"$set": {'is_greenlit':0}})
                flash('those two will never work together, try again!')
            else:
                _pitches.update( {'_id': ObjectId(pitch_id)},
                {"$set": {'is_greenlit':random_is_greenlit}})
                flash("how did you do?")
    return redirect(url_for('user_pitches'))


@app.route('/up_votes/<pitch_id>', methods=["POST", "GET"])
def up_votes(pitch_id):
    current_user = session.get('username')
    pitch_in_votes = _votes.count({'pitch_id': ObjectId(pitch_id)})
    voters = _votes.find_one({'pitch_id':ObjectId(pitch_id)})
    pitches = _pitches.find_one({'pitch_id':ObjectId(pitch_id)})

    if session.get('logged_in') == True:
        if pitch_in_votes == 0: # and current_user != pitches.username
            _votes.insert_one({ 'pitch_id': ObjectId(pitch_id), 'voters': [current_user] } )
            _pitches.update({ '_id': ObjectId(pitch_id) },{"$inc": {'votes': 1} } )
    # elif pitch_in_votes == 0 and pitches.username == current_user:
        # _votes.insert_one({ 'pitch_id': ObjectId(pitch_id), 'voters': [current_user] } )
        elif pitch_in_votes > 0 and current_user in voters['voters']:
            _votes.update(
                {'pitch_id': ObjectId(pitch_id) },
                {'$pull': { 'voters': current_user } } )
            _pitches.update({'_id': ObjectId(pitch_id) },{"$inc": {'votes': -1} } )
        else:
            _votes.update(
                {'pitch_id': ObjectId(pitch_id) },
                {'$push': { 'voters': current_user } } )
            _pitches.update({'_id': ObjectId(pitch_id) },{"$inc": {'votes': 1} } )
        return redirect(url_for('all_pitches') )
    flash('Please log in or register to vote')
    return redirect(url_for('all_pitches') )


@app.route('/hide_pitch/<pitch_id>', methods=["POST"])
def hide_pitch(pitch_id):
    pitches = mongo.db.pitches
    pitches.update( {'_id': ObjectId(pitch_id)},
    {"$set": {
        'is_del':True
    }})
    flash('Your pitch has been removed from further consideration!')
    return redirect(url_for('user_pitches'))


@app.route('/delete_pitch', methods=["POST"])
def delete_pitch():
    pitches = mongo.db.pitches
    pitches.remove({'is_del': True})
    flash('Hey Admin, you have flushed out the deleted pitches!')
    return redirect(url_for('user_pitches'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.getenv('DEBUG'))
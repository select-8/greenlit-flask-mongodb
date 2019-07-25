import os
from flask import Flask, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
@app.route('/show_user')
def show_user():
    return render_template("show_users.html", users=mongo.db.users.find())


@app.route('/add_pitch')
def add_pitch():
    _genres = mongo.db.genres.find()
    genre_list = [genre for genre in _genres]
    _directors = mongo.db.directors.find()
    director_list = [directors for directors in _directors]
    _actors = mongo.db.talent.find()
    actor_list = [actors for actors in _actors]
    return render_template('add_pitch.html', genres = genre_list, directors = director_list, actors=actor_list)


@app.route('/user_pitch', methods=['POST'])
def user_pitch():
    now = datetime.now()
    created_at = now.strftime("%d/%m/%Y %H:%M:%S")
    usercoll = mongo.db.users
    username = session['username']
    the_user = usercoll.find_one({'username': username})
    pitch = mongo.db.pitches
    title = request.form.get('title')
    genre_name = request.form.get('genre_name')
    director_name = request.form.get('director_name')
    actor_name = request.form.get('actor')
    description = request.form.get('discription')
    pitch.insert_one({'user_id': the_user['_id'], 'created_at': created_at, 'title': title,
                      'genre_name': genre_name, 'director_name': director_name,
                      'actor': actor_name, 'description': description, 
                      'tag':{'film1':{'title':'title1', 'img':''},'film2':{'title':'title2', 'img':''},'location':'testloc'}})
    return redirect(url_for('add_pitch'))


# @app.route('/add_pitch/<username>/<title>/<desc>/<director>/<actor>')
# def insert_pitch(username, title, desc, director, actor):
#     user = mongo.db.users
#     the_user = users.find_one({'username' : username})
#     the_pitch = mongo.db.pitches
#     the_pitch.insert({'username': the_user['username'], 'title': title, 'description': desc, 'director': director, 'actor': actor})
#     return redirect(url_for('show_pitches'))

@app.route('/show_pitches')
def show_pitches():
    return render_template("show_pitches.html", pitches=mongo.db.pitches.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.getenv('PORT'),
            debug=True)
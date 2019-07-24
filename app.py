import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config["MONGO_DBNAME"] = 'greenlit'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/add_user')
def add_user():
    user_collection = mongo.db.users
    user_collection.insert({"username":"Barry Barington"})
    user_collection.insert({"username":"Mary Maryington"})
    user_collection.insert({"username":"Johnny Johns"})
    return redirect(url_for('show_user'))

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
    pitch = mongo.db.pitches
    pitch.insert_one(request.form.to_dict())
    return redirect(url_for('add_pitch'))

@app.route('/add_pitch/<username>/<title>/<desc>/<director>/<actor>')
def insert_pitch(username, title, desc, director, actor):
    user = mongo.db.users
    the_user = user.find_one({'username' : username})
    the_pitch = mongo.db.pitches
    the_pitch.insert({'username': the_user['username'], 'title': title, 'description': desc, 'director': director, 'actor': actor})
    return redirect(url_for('show_pitches'))


@app.route('/show_pitches')
def show_pitches():
    return render_template("show_pitches.html", pitches=mongo.db.pitches.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.getenv('PORT'),
            debug=True)
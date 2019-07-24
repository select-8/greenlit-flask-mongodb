import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

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

@app.route('/show_user')
"""
should show session user and list of pitches with option to edit
and maybe to add a profile?
"""
def show_user():
    return render_template("show_users.html", users=mongo.db.users.find())

@app.route('/show_pitches')
def show_pitches():
    return render_template("show_pitches.html", pitches=mongo.db.pitches.find())


@app.route('/add_pitch/<username>/<title>/<desc>/<director>/<actor>')
def add_pitch(username, title, desc, director, actor):
    user = mongo.db.users
    the_user = user.find_one({'username' : username})

    the_pitch = mongo.db.pitches
    the_pitch.insert({'username': the_user['username'], 'title': title, 'description': desc, 'director': director, 'actor': actor})

    return redirect(url_for('show_pitches'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.getenv('PORT'),
            debug=True)
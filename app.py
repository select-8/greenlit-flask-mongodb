import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'greenlit'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert_one({'username': 'Tim'})
    return redirect(url_for('get_user'))

@app.route('/show_user')
def get_user():
    return render_template("show_users.html", users=mongo.db.users.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5001,
            debug=True)
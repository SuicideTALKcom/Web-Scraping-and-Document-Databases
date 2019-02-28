from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def get():
    mars = mongo.db.mars
    marsdata = scrape_mars.scrape()
    mars.update({}, marsdata, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run()
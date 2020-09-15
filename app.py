#Initial Set up
from flask import Flask, render_template, redirect
from pymongo import MongoClient
import scrape_mars

#Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = conn = "mongodb://localhost:27017/mars_data
mongo = MongoClient("mongodb://localhost:27017/mars_data")
app = Flask(__name__)

@app.route('/')
def home():
    mars_db = mongo.db.collection.find_one()
    return render_template ("index.html", mars = mars_db)

@app.route('/scrape')
def scrape():
    #images = mongo.db.collection
    images_data = scrape_mars.scrape()
    mongo.db.collection.update({}, images_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__, static_folder = "assets")

app.config["MONGO_URI"] = "mongodb://localhost:27017/bfo_papers"
mongo = PyMongo(app)



@app.route("/")
def index():
    bfo_papers = mongo.db.bfo_papers.find_one()
    return render_template("index.html", bfo_papers = bfo_papers)


@app.route("/scrape")
def scraper():
    bfo_papers = mongo.db.bfo_papers
    new_papers = scrape.scrape()
    print(new_papers)
    bfo_papers.update_one({}, {"$set": new_papers}, upsert=True) 
#     # new_papers = jsonify(new_papers)
#     #return {'data': new_papers}
#     # return new_papers
    return redirect("/", code=302)

# @app.route("/get-data")
# def data(): 
#     return {'data': new_papers}

if __name__ == "__main__":
    app.run(debug=True)

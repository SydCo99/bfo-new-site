from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    Authors = Col('Authors')
    Date = Col('Date')
    Title = Col('Title')
    Publication = Col('Publication')
    Link = Col('Link')


app = Flask(__name__, static_folder = "assets")

app.config["MONGO_URI"] = "mongodb://localhost:27017/bfo_papers"
mongo = PyMongo(app)



@app.route("/")
def index():
    bfo_papers = mongo.db.bfo_papers.find_one()
    #call back the lists here 
    #print(bfo_papers)
    bfo_authors = bfo_papers["Authors"]
    bfo_titles = bfo_papers["Title"]
    bfo_dates = bfo_papers["Date"]
    bfo_pub = bfo_papers["Publication"]
    bfo_links = bfo_papers["Link"]
    array_data = []
    for i in range(len(bfo_titles)):
        row = []
        row.append(bfo_authors[i])
        row.append(bfo_titles[i])
        row.append(bfo_dates[i])
        row.append(bfo_pub[i])
        row.append(bfo_links[i])
        array_data.append(row)
        row = []
        i += 1 
    
    return render_template("index.html", array_data = array_data )


@app.route("/scrape")
def scraper():
    bfo_papers = mongo.db.bfo_papers
    new_papers = scrape.scrape()
    #print(new_papers)
    bfo_papers.update_one({}, {"$set": new_papers}, upsert=True) 
#     # new_papers = jsonify(new_papers)
#     #return {'data': new_papers}
#     # return new_papers
    return redirect("../#whats-new", code=302)

@app.route("/publications-full")
def publications(): 
    return render_template("inner-page.html")

# @app.route("/get-data")
# def data(): 
#     return {'data': new_papers}

if __name__ == "__main__":
    app.run(debug=True)

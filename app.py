from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape
from flask_table import Table, Col
import pandas as pd 

# Declare your table
class ItemTable(Table):
    Authors = Col('Authors')
    Date = Col('Date')
    Title = Col('Title')
    Publication = Col('Publication')
    Link = Col('Link')


app = Flask(__name__, static_folder = "assets")
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/bfo_papers"
# mongo = PyMongo(app)


@app.route("/")
def index():
    # bfo_papers = mongo.db.bfo_papers.find_one()
    # #call back the lists here 
    # #print(bfo_papers)
    # bfo_authors = bfo_papers["Authors"]
    # bfo_titles = bfo_papers["Title"]
    # bfo_dates = bfo_papers["Date"]
    # bfo_pub = bfo_papers["Publication"]
    # bfo_links = bfo_papers["Link"]
    # array_data = []
    # for i in range(len(bfo_titles)):
    #     row = []
    #     row.append(bfo_authors[i])
    #     row.append(bfo_titles[i])
    #     row.append(bfo_dates[i])
    #     row.append(bfo_pub[i])
    #     row.append(bfo_links[i])
    #     array_data.append(row)
    #     row = []
    #     i += 1 
    df1 = pd.read_csv("assets/newpubs.csv")
    authors = df1["Authors"].tolist()
    titles = df1["Title"].tolist()
    date = df1["Date"].tolist()
    pub = df1["Publication"].tolist()
    link = df1["Link"].tolist()
    for i in range(len(authors)):
        authors[i] = authors[i].strip('[')
        authors[i] = authors[i].strip(']')
        authors[i] = eval(authors[i])
    array_data = []
    for i in range(len(titles)):
        row = []
        row.append(authors[i])
        row.append(titles[i])
        row.append(date[i])
        row.append(pub[i])
        row.append(link[i])
        array_data.append(row)
        row = []
        i += 1 

    return render_template("index.html", array_data = array_data )


@app.route("/scrape")
def scraper():
    # bfo_papers = mongo.db.bfo_papers
    # new_papers = scrape.scrape()
    # bfo_papers.update_one({}, {"$set": new_papers}, upsert=True) 

    return redirect("../#whats-new", code=302)

# @app.route("/publications-full")
# def publications(): 
#     return render_template("inner-page.html")

@app.route("/users")
def user(): 
    df = pd.read_csv("assets/users.csv")
    df = df.drop(columns = ["description", "underneath"])
    df = df.sort_values('name', ascending = True)
    df["url"] = df["url"].fillna("no_link")
    users = df.to_dict(orient='records')
    for user in users: 
        if user["url"] == "no_link": 
            del user['url']
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)



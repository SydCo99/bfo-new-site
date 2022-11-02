import requests
import pandas as pd
from config import api_key, user_id
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    articles = {}
    url = "https://philpapers.org/browse/top-level-ontologies"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    full_citation_list = soup.find_all("span", class_="citation")
    html = []  
    for i in range(len(full_citation_list)):
        html.append(full_citation_list[i])
    authors = []
    titles = []
    pub_date = []
    pub_info = []
    links = []

    for entry in html: 
        #for hit in entry.find_all("span", class_="name"): 
            #authors.append(hit.contents[0].strip())
        # for author in entry.find_all("span", class_="name"):
        #     authors.append(''.join(author.findAll(text=True)))
        authors.append(entry.find_all("span", class_="name"))
        titles.append(entry.find("span", class_="articleTitle").text)
        pub_date.append(entry.find("span", class_="pubYear").text)
        pub_info.append(entry.find("span", class_="pubInfo").text)
        link = entry.find("a", href=True)
        links.append("https://philpapers.org" + link["href"])
        
    entries = []

    for publication in range(len(titles)):
        case = {"author": authors[publication], "title": titles[publication], "pub_date": pub_date[publication],
                "pub_info": pub_info[publication], "links": links[publication]}
        entries.append(case)

    browser.quit()
        
    print(entries)
    
    

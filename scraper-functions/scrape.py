import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import csv 

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    url = "https://philpapers.org/browse/top-level-ontologies?limit=50&newWindow=&publishedOnly=&freeOnly=&catq=barry+smith&hideAbstracts=&langFilter=&filterByAreas=&sqc=&proOnly=on&uncat=&cn=top-level-ontologies&onlineOnly=&cId=492826&categorizerOn=&new=1&start=0&setAside=&sort=pubYear&showCategories=on&format=html&jlist=&ap_c1=&ap_c2="
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    full_citation_list = soup.find_all("span", class_="citation")
    html = []  
    for i in range(len(full_citation_list)):
        html.append(full_citation_list[i])
    author_full = []
    titles = []
    pub_date = []
    pub_info = []
    links = []
    authors = []
    titles_full = []
    pub_info_full = []

    for entry in html: 
        author_full.append(entry.find_all("span", class_="name"))
        titles_full.append(entry.find("span", class_="articleTitle").text)
        pub_date.append(entry.find("span", class_="pubYear").text)
        pub_info_full.append(entry.find("span", class_="pubInfo").text)
        link = entry.find("a", href=True)
        links.append("https://philpapers.org" + link["href"])
        
    for i in range(len(pub_info_full)): 
        line = pub_info_full[i]
        line = line.replace('.','')
        pub_info.append(line)
        i += 1
    for i in range(len(titles_full)): 
        line = titles_full[i]
        line = line.replace('.','')
        titles.append(line)
        i += 1

    author_full = list(map(str, author_full))
    for i in range(len(author_full)): 
        line = striphtml(author_full[i])
        #line = line.replace(', ', ',')
        line = line.replace(' ]', ']')

        authors.append(line)
        i += 1

    for i in range(len(authors)):
        authors[i] = authors[i].strip('][').split(',')
        
    phil_authors = []
    phil_titles = []
    phil_pub_date = []
    phil_pub_info = []
    phil_links = []
    
    phil_authors = authors
    phil_titles = titles 
    phil_pub_date = pub_date 
    phil_pub_info = pub_info 
    phil_links = links 
        
#     entries = []

#     for publication in range(len(titles)):
#         case = {"author": authors[publication], "title": titles[publication], "pub_date": pub_date[publication],
#                 "pub_info": pub_info[publication], "links": links[publication]}
#         entries.append(case)
   
    browser.quit()
    
    time.sleep(1)
    
    #start of scilit scraper 
    executable_path = {'executable_path': ChromeDriverManager().install()}
  
    browser = Browser('chrome', **executable_path, headless=True)
    
    url = "https://www.scilit.net/articles/search?facets__language%5B0%5D=English&highlight=1&q=%22basic%20formal%20ontology%22&sort=Newest&nb_articles=500"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    full_citation_list = soup.find_all("div", class_="result")
    
    html = []  
    for i in range(len(full_citation_list)):
        html.append(full_citation_list[i])
        
    authors = []
    titles = []
    titles_full = []
    pub_date = []
    pub_info = []
    links = []
    author_full = []
    pub_date_full = []
    pub_info_full = []
    links_full = []

    for entry in html: 
        author_full.append(entry.find_all("div", class_="authors"))
        titles_full.append(entry.find("div", class_="title").text)
        pub_date_full.append(entry.find("div", class_="pubdate").text)
        pub_info_full.append(entry.find("div", class_="publisher"))
        #links.append(entry.find("div", class_="doilink"))
        link = entry.find("a", href=True)
        links_full.append(link)    
        
    for i in range(len(links_full)):
        link = links_full[i]["href"]
        links.append("https://www.scilit.net"+ link)
        i =+ 1
        
    pub_info_full = list(map(str, pub_info_full))
    for i in range(len(pub_info_full)):
        line = striphtml(pub_info_full[i])
        line = line.replace('by\n', '')
        line = line.replace('\n', '')
        pub_info.append(line)
        i += 1
    for i in range(len(pub_date_full)):
        line = pub_date_full[i]
        line = line.replace('Published: ', '')
        pub_date.append(line)
        i += 1

    for i in range(len(pub_date)):
        if pub_date[i] == "unknown date": 
            pub_date[i] = "0 - Date Unknown"
            i += 1
        else: 
            pub_date[i] = pub_date[i][-4:]
            i += 1 
        
    for i in range(len(titles_full)):
        line = titles_full[i]
        line = line.replace('\n', '')
        titles.append(line)
        i += 1
    author_full = list(map(str, author_full))
    for i in range(len(author_full)): 
        line = striphtml(author_full[i])
        line = line.replace('\n', '')
        line = line.replace(' ]', ']')
        line = line.replace(',',', ')

        authors.append(line)
        i += 1

    for i in range(len(authors)):
        authors[i] = authors[i].strip('][').split(',')
        
    for x in phil_authors:
        authors.append(x)
    for x in phil_titles:
        titles.append(x)
    for x in phil_pub_date:
        pub_date.append(x)
    for x in phil_pub_info:
        pub_info.append(x)
    for x in phil_links: 
        links.append(x)
        
    articles = {}
    articles["Authors"] = authors
    articles["Title"] = titles
    articles["Date"] = pub_date
    articles["Publication"] = pub_info
    articles["Link"] = links
        
    # for publication in range(len(titles)):
    #     case = {"author": authors[publication], "title": titles[publication], "pub_date": pub_date[publication],
    #             "pub_info": pub_info[publication], "links": links[publication]}
    #     entries.append(case)
    df = pd.DataFrame(articles)
    df.to_csv("assets/newpubs.csv", index = False, quoting = csv.QUOTE_NONE, escapechar = ' ')

    browser.quit()
    # print(f"length of entries list is: {len(entries)}")
    # print(entries)

    df1 = pd.read_csv("assets/newpubs.csv", escapechar = ' ')
    authors = df1["Authors"].tolist()
    titles = df1["Title"].tolist()
    date = df1["Date"].tolist()
    pub = df1["Publication"].tolist()
    link = df1["Link"].tolist()
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
    print(array_data)

scrape()





    

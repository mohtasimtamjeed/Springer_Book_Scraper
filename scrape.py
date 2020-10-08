import requests
import re
from bs4 import BeautifulSoup
from csv import writer
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get("http://localhost:9000/html.html", headers)

dataArr = []

soup = BeautifulSoup(response.text, "html.parser")

for post in soup.findAll(href=re.compile("link.springer.com")):
    dataArr.append(post.contents[0])
    

print(len(dataArr))

for id, data in enumerate(dataArr):
    print(id)
    if id > 346:

        page = requests.get(data)

        rootUrl = "http://link.springer.com"

        newSoup = BeautifulSoup(page.text, "html.parser")
        bookTitle = newSoup.find(attrs={"data-test":"book-title"}).get_text()
        bookUrl = newSoup.find("a", attrs={"data-track-action":"Book download - pdf"}).get("href")

        authorSoup = newSoup.find("div", class_="persons__list")
        

        bookAuthors = []
        for author in authorSoup.findAll("span", class_="authors__name"):
            bookAuthors.append(author.get_text().replace("\xa0", " ").split())

        authorString = ""
        if len(bookAuthors) > 1:
            for author in bookAuthors:
                #print(author[-1])
                authorString += author[-1] + " "
        else:
            authorString = " ".join(bookAuthors[0]) 

        dlUrl = rootUrl + bookUrl

        saveName = authorString + "_" + bookTitle + ".pdf"
        saveName = saveName.replace("\n", "")
        saveName = saveName.replace("/", "")
        
        print(dlUrl)
        
        
        r = requests.get(dlUrl, stream = True)

        with open(saveName, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk) 

        print(id, "downloaded")
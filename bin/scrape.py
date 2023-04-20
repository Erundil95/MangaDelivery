import requests
from bs4 import BeautifulSoup

#Mango to download
mangas_to_dl = ["Jujutsu Kaisen"]

#URL manga website
base_url = "https://onepiecechapters.com"
mangalist_url = "https://onepiecechapters.com/projects"

response = requests.get(mangalist_url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

title = soup.find("title").get_text()
description = soup.find("meta", {"name": "description"})
["content"]

manga_divs = soup.find_all("div", {"class": "flex flex-col"})

for manga_div in manga_divs:
    for manga in mangas_to_dl:      
        title = manga_div.find("a").get_text()
        if(title == manga):                                    #TODO: look to make the search more smart for japanese names variants
            print(title)
            chapter_list_url = base_url + manga_div.find("a")["href"]
            print(chapter_list_url)
            chapter_list_content = requests.get(chapter_list_url).content
            # print(chapter_list_content)
    
    #print("Manga title:", title)


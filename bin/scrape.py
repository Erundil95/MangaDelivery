import requests
import re
import os
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Constants
BASE_URL = "https://onepiecechapters.com"
MANGALIST_URL = "https://onepiecechapters.com/projects"
TITLES_TO_DOWNLOAD = ["Jujutsu Kaisen"]
SAVE_FOLDER = r"D:\Documents\MangaDelivery"

def replace_special_numbers(string):
    pattern = r'[①-⑳]'  # match any circled number from 1 to 20
    char_map = {'①': '1', '②': '2', '③': '3', '④': '4', '⑤': '5',
                '⑥': '6', '⑦': '7', '⑧': '8', '⑨': '9', '⑩': '10',
                '⑪': '11', '⑫': '12', '⑬': '13', '⑭': '14', '⑮': '15',
                '⑯': '16', '⑰': '17', '⑱': '18', '⑲': '19', '⑳': '20'}
    return re.sub(pattern, lambda match: char_map[match.group()], string)


# If main directory doens't exist then create it
if not os.path.exists(SAVE_FOLDER):                   # TODO: add a folder icon for the luls
    os.mkdir(SAVE_FOLDER, 0o777)


# Send a GET request to the manga website main page
response = requests.get(MANGALIST_URL)
response.raise_for_status()
html_content = response.content

# Parse HTML content 
soup = BeautifulSoup(html_content, "html.parser")

# Find all mangas available
manga_divs = soup.find_all("div", {"class": "flex flex-col"})

# Loop over each manga on the website to match the desired ones
for manga_div in manga_divs:
    for manga in TITLES_TO_DOWNLOAD:      
        title = manga_div.find("a").get_text()

        if(title == manga):                                                 
            #TODO: look to make the search more smart for japanese names variants
            manga_title_dir = os.path.join(SAVE_FOLDER, manga)
            chapter_list_url = BASE_URL + manga_div.find("a")["href"]
            chapter_list_response = requests.get(chapter_list_url)
            chapter_list_response.raise_for_status()
            
            chapter_list_soup = BeautifulSoup(chapter_list_response.content, "html.parser")

            # Save all chapter blocks with Link, Chapter number and Chapter title
            for link in chapter_list_soup.find_all("a", href=re.compile(r"/chapters/\d+/.+")):
                i = 0
                # Get the chapter number by splitting the link with / and then -
                chapter_number = link['href'].split('/')[-1].split('-')[-1]
                chapter_link = link['href']
                chapter_title = link.get_text().replace("Jujutsu Kaisen ", "").replace('\n', ' ').replace('\r', ' ').strip()
                chapter_title = replace_special_numbers(chapter_title)

                # Create Chapter directory if not exists
                chapter_dir = os.path.join(manga_title_dir, f"{chapter_title}")           
                if not os.path.exists(chapter_dir):
                     os.makedirs(chapter_dir)

                # Skip chapter if the folder isn't empty       #TODO: Manage case when a chapter is half written, count the img in the chpater vs img in the folder
                if os.listdir(chapter_dir):
                    print(f"{chapter_dir}" + "already exists and is not empty, skipping... ")     
                else:
                    print("Downloading " + f"{chapter_dir}")
                    chapter_response = requests.get(BASE_URL + chapter_link)
                    chapter_response.raise_for_status()

                    chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")

                    image_links = chapter_soup.find_all("img", {"class": "fixed-ratio-content"})

                    # Gather all the images that make up the chapter
                    for image_link in enumerate(image_links):
                        image_url = image_link['src']
                        # image_name = f"{i + 1}" + ".jpg"
                        image_response = requests.get(image_url)
                        
                        # Save the images in the local folder
                        if image_response.status_code == 200:
                            # Open the image using Pillow
                            img = Image.open(BytesIO(image_response.content))

                            # Convert the image to the RGB mode
                            img = img.convert('RGB')

                            # Save the image to a local file as JPEG
                            img.save(os.path.join(chapter_dir, image_name), 'JPEG')
                            print('Image saved successfully!')
                        else:
                            print('Failed to download image')

                if(i>1):
                    break
                



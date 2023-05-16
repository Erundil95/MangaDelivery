import requests
import re
import os
import io
import zipfile
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

import sys

class OnePieceChaptersScraper(BaseScraper):
    
    def __init__(self, config):
        super().__init__(config)
        self.BASE_URL = config['base_url']
        self.MANGALIST_URL = config['mangalist_url']
        self.TITLES_TO_DOWNLOAD = config['titles_to_download']
        self.SAVE_FOLDER = config['save_folder']
        self.SAVE_FORMAT = config['save_format']

        # print("BASE_URL:", self.BASE_URL)
        # print("MANGALIST_URL:", self.MANGALIST_URL)
        # print("TITLES_TO_DOWNLOAD:", self.TITLES_TO_DOWNLOAD)
        # print("SAVE_FOLDER:", self.SAVE_FOLDER)
        # print("SAVE_FORMAT:", self.SAVE_FORMAT)

    def create_save_folder(self):
    # If main directory doens't exist then create it
        if not os.path.exists(self.SAVE_FOLDER):                   # TODO: add a folder icon for the luls
            os.mkdir(self.SAVE_FOLDER, 0o777)

    def get_manga_divs(self):
        # Send a GET request to the manga website main page
        response = requests.get(self.MANGALIST_URL)
        response.raise_for_status()
        html_content = response.content

        # Parse HTML content 
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all mangas available
        manga_divs = soup.find_all("div", {"class": "flex flex-col"})
        return manga_divs

    def download_manga(self, manga_divs):
    # Loop over each manga on the website to match the desired ones
        for manga_div in manga_divs:
            for manga in self.TITLES_TO_DOWNLOAD:   
                # Extract manga title   
                title = manga_div.find("a").get_text()

                if(title == manga):                                                 
                #TODO: look to make the search more smart for japanese names variants
                    print(manga + " found, downloading...")
                    self.download_chapters(manga_div, manga)

    def get_chapter_info(self, manga_div):
    # Get the list of div for each chapter (includes: chapter_title, chapter_number, chapter_link)  
        chapter_list_url = self.BASE_URL + manga_div.find("a")["href"]
        chapter_list_response = requests.get(chapter_list_url)
        chapter_list_response.raise_for_status()
        chapter_list_soup = BeautifulSoup(chapter_list_response.content, "html.parser")

        chapter_info = []
        for link in chapter_list_soup.find_all("a", href=re.compile(r"/chapters/\d+/.+")):
         # Get the chapter number by splitting the link with / and then -
            chapter_number = link['href'].split('/')[-1].split('-')[-1]
            chapter_link = link['href']
            chapter_title = link.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', '').replace(':', '').strip()  #TODO: Remove Manga title form the chapter name (chapter name is Manga name + Chapter N* + title)
            chapter_title = self.replace_special_numbers(chapter_title)

            chapter_info.append((chapter_link, chapter_title, chapter_number))

        return chapter_info
    
    def create_chapter_directory(self, manga, chapter_title):
        chapter_dir = os.path.join(self.SAVE_FOLDER, manga, chapter_title)

        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        return chapter_dir

    def download_chapters(self, manga_div, manga):
            chapter_list = self.get_chapter_info(manga_div)

            # Switch dictionary with savefile methods
            switch_dict = {
                'cbz': self.save_images_as_cbz,
                'pdf': self.save_images_as_pdf
            }

            # Save all chapter blocks with Link, Chapter number and Chapter title
            for chapter_link, chapter_title, chapter_number in chapter_list:
                chapter_dir = self.create_chapter_directory(manga, chapter_title.replace(manga, ''))

                # Skip chapter if the folder isn't empty       # TODO: Manage case when a chapter is half written, count the img in the chpater vs img in the folder
                if os.listdir(chapter_dir):
                    print(f"{chapter_dir}" + "already exists and is not empty, skipping... ")  

                else:
                    print("Downloading " + f"{chapter_dir}")

                    chapter_response = requests.get(self.BASE_URL + chapter_link)
                    chapter_response.raise_for_status()

                    chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
                    image_links = chapter_soup.find_all("img", {"class": "fixed-ratio-content"})

                    images = self.download_images(image_links)

                    save_function = switch_dict.get(self.SAVE_FORMAT, self.save_images_as_cbz)
                    save_function(images, chapter_dir, chapter_title)

                    sys.exit()


    def download_images(self, image_links):
        images = []
        for i, image_link in enumerate(image_links):
            image_url = image_link['src']
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                with Image.open(BytesIO(image_response.content)) as img:
                    img = img.convert('RGB')

                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    img_bytes = img_byte_arr.getvalue()

                    images.append((f"page{i + 1}.jpg", img_bytes))
            else:
                print('Failed to download image')

        return images
    
    def save_images_as_cbz(self, images, chapter_dir, chapter_title):
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_name, img_bytes in images:
                zip_file.writestr(file_name, img_bytes)

        zip_file_name = f"{chapter_title}.cbz"
        zip_buffer.seek(0)

        with open(os.path.join(chapter_dir, zip_file_name), "wb") as zip_file:
            zip_file.write(zip_buffer.read())

    def save_images_as_pdf(self, images, chapter_dir, chapter_title):
        return False

    def start_download(self):
        self.create_save_folder()
        manga_divs = self.get_manga_divs()
        self.download_manga(manga_divs)
import re
import os
import io
import zipfile
from io import BytesIO
from PIL import Image
from utils import utils
import sys
from core.request_handler import RequestHandler
from core.image_saver import Image_saver
from .base_scraper import BaseScraper

class MangaScraper(BaseScraper):
    def __init__(self, config):
        self.BASE_URL = config['base_url']
        self.MANGALIST_URL = config['mangalist_url']
        self.TITLES_TO_DOWNLOAD = config['titles_to_download']
        self.SAVE_FOLDER = config['save_folder']
        self.SAVE_FORMAT = config['save_format']

    def get_manga_list(self):
        # Send a GET request to the manga website main page
        html_content = RequestHandler.send_request(self.MANGALIST_URL)

        # Parse HTML content 
        soup = RequestHandler.parse_html(html_content)

        # Find all mangas available
        manga_list = soup.find_all("div", {"class": "flex flex-col"})
        return manga_list

    def download_mangas(self, manga_list):
    # Loop over each manga on the website to match the desired ones
        for manga_div in manga_list:
            for manga in self.TITLES_TO_DOWNLOAD:   
                # Extract manga title   
                title = manga_div.find("a").get_text()

                if(title == manga):                                                 
                #TODO: look to make the search more smart for japanese names variants
                    print(manga + " found, downloading...")
                    self.download_chapters(manga_div, manga)

    def download_chapters(self, manga_div, manga):
            chapter_list = self.get_chapter_info(manga_div)

            # Switch dictionary with savefile methods
            switch_dict = {
                'cbz': Image_saver.save_images_as_cbz,
                'pdf': Image_saver.save_images_as_pdf
            }

            # Save all chapter blocks with Link, Chapter number and Chapter title
            for chapter_link, chapter_title, chapter_number in chapter_list:
                chapter_dir = os.path.join(self.SAVE_FOLDER, manga, chapter_title.replace(manga, ''))

                utils.create_save_folder(chapter_dir)

                # Skip chapter if the folder isn't empty       # TODO: Manage case when a chapter is half written, count the img in the chpater vs img in the folder
                if os.listdir(chapter_dir):
                    print(f"{chapter_dir}" + "already exists and is not empty, skipping... ")  

                else:
                    print("Downloading " + f"{chapter_dir}")

                    chapter_response = RequestHandler.send_request(self.BASE_URL + chapter_link)

                    chapter_soup = RequestHandler.parse_html(chapter_response)
                    image_links = chapter_soup.find_all("img", {"class": "fixed-ratio-content"})

                    images = self.download_images(image_links)

                    save_function = switch_dict.get(self.SAVE_FORMAT, Image_saver.save_images_as_cbz)
                    save_function(images, chapter_dir, chapter_title)

                    #TODO: REMOVE THIS TEST ONLY
                    sys.exit()

    def get_chapter_info(self, manga_div):
    # Get the list of div for each chapter (includes: chapter_title, chapter_number, chapter_link)  
        chapter_list_url = self.BASE_URL + manga_div.find("a")["href"]
        chapter_list_response = RequestHandler.send_request(chapter_list_url)

        chapter_list_soup = RequestHandler.parse_html(chapter_list_response)

        chapter_info = []
        for link in chapter_list_soup.find_all("a", href=re.compile(r"/chapters/\d+/.+")):
         # Get the chapter number by splitting the link with / and then -
            chapter_number = link['href'].split('/')[-1].split('-')[-1]
            chapter_link = link['href']
            chapter_title = link.get_text().replace('\n', ' ').replace('\r', ' ').replace(',', '').replace(':', '').strip()  #TODO: Remove Manga title form the chapter name (chapter name is Manga name + Chapter N* + title)
            chapter_title = utils.replace_special_numbers(chapter_title)

            chapter_info.append((chapter_link, chapter_title, chapter_number))

        return chapter_info

    def download_images(self, image_links):
        images = []
        for i, image_link in enumerate(image_links):
            image_url = image_link['src']
            image_content = RequestHandler.send_request(image_url)

            if image_content != None:
                with Image.open(BytesIO(image_content)) as img:
                    img = img.convert('RGB')

                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    img_bytes = img_byte_arr.getvalue()

                    images.append((f"page{i + 1}.jpg", img_bytes))
            else:
                print('Failed to download image')

        return images

    def start_download(self):
        utils.create_save_folder(self.SAVE_FOLDER)
        manga_list = self.get_manga_list()
        self.download_mangas(manga_list)
from abc import ABC, abstractclassmethod
from config.config_loader import ConfigLoader


import os

ALL_CHAPTERS = 99999

class BaseScraper(ABC):

    @property
    @abstractclassmethod
    def get_base_url(self):
        pass
    
    @abstractclassmethod
    def start_download(self):
        pass

    @abstractclassmethod
    def get_manga_list(self):
        pass

    @abstractclassmethod
    def download_mangas(self, manga_list):
        pass

    @abstractclassmethod
    def download_chapters(self, manga_div, manga):
        pass

    @abstractclassmethod
    def get_chapter_info(self, manga_div):
        pass

    @abstractclassmethod
    def download_images(self, image_links):
        pass

    def check_max_chapters(self, manga_div, manga):
        config_loader = ConfigLoader()

        max_chapters = config_loader.get_setting('titles_to_download')[manga]
        if max_chapters == 0:
            self.download_chapters(manga_div, manga, max_chapters=ALL_CHAPTERS)
            config_loader.set_chapters_to_download_default(manga)
        else:
            self.download_chapters(manga_div, manga, max_chapters)
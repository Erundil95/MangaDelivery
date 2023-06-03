from abc import ABC, abstractclassmethod

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

    
from abc import ABC, abstractmethod


class BaseScraper:
    """
    Abstract class defining the methods that any manga scraper should have.
    """

    def __init__(self, base_url, manga_list_url, titles_to_download, save_folder):
        """
        Args:
            base_url (str): The base URL of the manga website.
            manga_list_url (str): The URL of the page listing all mangas.
            titles_to_download (list of str): The titles of the mangas to download.
            save_folder (str): The path of the folder where mangas should be saved.
        """
        self.base_url = base_url
        self.manga_list_url = manga_list_url
        self.titles_to_download = titles_to_download
        self.save_folder = save_folder

    def get_manga_list(self):
        """Gets the list of all mangas available on the website.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


    def get_chapter_list(self, manga_title):
        """Gets the list of all chapters of a specific manga.

        Args:
            manga_title (str): The title of the manga.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


    def download_chapter(self, manga_title, chapter_number):
        """Downloads a specific chapter of a specific manga.

        Args:
            manga_title (str): The title of the manga.
            chapter_number (int): The number of the chapter.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

from abc import ABC, abstractclassmethod

class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url
    
    
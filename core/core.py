import sys
from scraper.onepiecechapters_scraper import OnePieceChaptersScraper
from config.config_loader import ConfigLoader
from utils import utils

def run():
    # Config = Dictionary <key_setting> : string/list <value>d
    # TODO: temporary, add support for different scrapers, run a search on which mangas each site has
    manga_scraper = OnePieceChaptersScraper()
    manga_scraper.start_download()
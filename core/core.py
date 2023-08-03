from scraper.onepiecechapters_scraper import OnePieceChaptersScraper
from config.config_loader import ConfigLoader
import cloudsave

import sys

def run():
    config = ConfigLoader()
    cloud_service = config.get_setting('cloud_service')
    mangas = config.get_setting('titles_to_download')

    # TODO: temporary, add support for different scrapers, run a search on which mangas each site has
    manga_scraper = OnePieceChaptersScraper()
    manga_scraper.start_download()

    if cloud_service:
        cloud_instance = cloudsave.base_cloud.BaseCloud.get_cloud_service(cloud_service)
        
        for manga_title in mangas.keys():
            cloud_instance.synch_files_with_local(manga_title)
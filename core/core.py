import os
import json
import sys
from scraper.manga_scraper import MangaScraper
from config.config_loader import ConfigLoader
from utils import utils

def run():
    # Load JSON config file = current_dir path + going up one level with '..' + config + config.json
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))

    try:
        config_loader = ConfigLoader(config_file_path)
        config = config_loader.load_config()
    except FileNotFoundError:
        print(f"@@ Config file not found at {config_file_path}")
        utils.create_default_config(config_file_path)
        sys.exit()

    # Config = Dictionary <key_setting> : string/list <value>d
    manga_scraper = MangaScraper(config)
    manga_scraper.start_download()
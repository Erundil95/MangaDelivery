import os
import json
import sys
from manga_scraper import MangaScraper
from config_loader import ConfigLoader

def create_default_config(config_file_path):
    default_config = {
        "save_folder": "MangaDeliveryTest",
        "base_url": "https://onepiecechapters.com",
        "mangalist_url": "https://onepiecechapters.com/projects",
        "titles_to_download": [],
        "save_format": "cbz"
    }

    print("Generating default one, please fill in the manga list")
    with open(config_file_path, 'w') as f:
        json.dump(default_config, f, indent=2)
    

if __name__ == "__main__":
    # Load JSON config file = current_dir path + going up one level with '..' + config + config.json
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json'))

    try:
        config_loader = ConfigLoader(config_file_path)
        config = config_loader.load_config()
    except FileNotFoundError:
        print(f"@@ Config file not found at {config_file_path}")
        create_default_config(config_file_path)
        sys.exit()


    # Config = Dictionary <key_setting> : string/list <value>d
    manga_scraper = MangaScraper(config)
    manga_scraper.start_download()
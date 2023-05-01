import os
import sys

from manga_scraper import MangaScraper
from config_loader import ConfigLoader

if __name__ == "__main__":
    # Load JSON config file = current_dir path + config + config.json
    print("STARTING")
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (exe)
        application_path = os.path.dirname(sys.executable)
        print("Running from executable bundle, config: " + application_path)
        config_file_path = os.path.join(application_path, 'config', 'config.json')
    else:
        # If the application is run from the source (Python interpreter)
        application_path = os.path.dirname(os.path.abspath(__file__))
        print("Running from source, config: " + application_path)
        config_file_path = os.path.join(application_path, '..', 'config', 'config.json')
    
    config_loader = ConfigLoader(config_file_path)
    print(config_file_path)
    config = config_loader.load_config()

    # Config = Dictionary <key_setting> : string/list <value>
    manga_scraper = MangaScraper(config)
    manga_scraper.start_download()
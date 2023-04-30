import requests
import re
import os
import io
import zipfile
import sys
import json
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from manga_scraper import MangaScraper
from config_loader import ConfigLoader

if __name__ == "__main__":
    # Load JSON config file = current_dir path + going up one level with '..' + config + config.json
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'config.json')
    config_loader = ConfigLoader(config_file_path)
    config = config_loader.load_config()

    # Config = Dictionary <key_setting> : string/list <value>d
    manga_scraper = MangaScraper(config)
    manga_scraper.start_download()
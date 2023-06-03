import requests
from  requests.exceptions import HTTPError, Timeout, ConnectionError
from bs4 import BeautifulSoup

class RequestHandler:
    @staticmethod
    def send_request(url):
        try:  
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP Error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"Error occurred: {err}")
            return None
        else:
            return response.content
        
    @staticmethod
    def parse_html(html_content):
        return BeautifulSoup(html_content, "html.parser")
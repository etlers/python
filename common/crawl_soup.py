import requests
from bs4 import BeautifulSoup as bs


def get_soup(url):
    response = requests.get( url, headers={"User-agent": "Mozilla/5.0"} )
    soup = bs(response.text, 'html.parser')

    return soup
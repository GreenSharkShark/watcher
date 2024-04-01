import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


def kinogo_by_parser(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            target: str = soup.find('span', class_='status7').text
            return target
        else:
            return "Service doesn't responding"
    except ConnectionError:
        return 'ConnectionError while requesting'

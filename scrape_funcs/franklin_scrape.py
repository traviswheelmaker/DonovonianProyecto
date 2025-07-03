import requests
from bs4 import BeautifulSoup
import bs4 #for type hints
from typing import Generator
def main() -> Generator[dict[str, str], None, None]:
    url: str = "https://clerk.franklincountyohio.gov/CLCT-website/media/Docs/PRRreports/ExcessSalesProceeds.html"
    source: str = requests.get(url).text
    soup: bs4.BeautifulSoup = BeautifulSoup(source, 'lxml')
    div_elements: bs4.element.ResultSet = soup.find_all('div', style="word-wrap:break-word;white-space:pre-wrap;")

    element_i: int = 0
    while element_i < len(div_elements):
        data: dict[str, str] = {
            "County": "Franklin",
            "Case Number": div_elements[element_i].get_text(),
            "Plantiff": div_elements[element_i+1].get_text(),
            "Defendant": div_elements[element_i+2].get_text(),
            "Sale Date": div_elements[element_i+3].get_text(),
            "Surplus Funds": div_elements[element_i+4].get_text()
        }
        yield data
        element_i += 5

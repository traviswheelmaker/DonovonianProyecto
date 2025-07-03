import requests, pdfplumber
from bs4 import BeautifulSoup
import bs4 #for type hints
from typing import Generator
def main() -> Generator[dict[str, str], None, None]:
    def get_main_source():
        url1: str = "https://dekalbtax.org/delinquent-tax"
        source1: str = requests.get(url1).text
        soup1: bs4.BeautifulSoup = BeautifulSoup(source1, 'lxml')
        element_list: bs4.element.ResultSet = soup1.findAll('a', target="_blank")

        element: bs4.element.Tag
        for element in element_list:
            if "excess" in (element.get_text()).lower():
                url2: str = element.get("href")
                source2: bytes = requests.get(url2).content #pdf
                file_path: str = "output/dekalb.pdf"
                with open(file_path, 'wb') as file:
                    file.write(source2)
                break
                
    get_main_source()

    file_path: str = "output/dekalb.pdf"
    with pdfplumber.open(file_path) as pdf:
        page: pdfplumber.page.Page
        for page in pdf.pages:
            arguments: dict[str, str|int] = {
                "vertical_strategy": "explicit",
                "horizontal_strategy": "lines",
                "explicit_vertical_lines": [
                    15, 70, 145, 185, 565, 610, 675, 820, 872, 950, 990
                ]
            }
            tables: list[list[str]] = page.extract_tables(arguments)[0]
            page.close()

            table: list[str]
            for table in tables[1::]:
                #parcelid, surplus funds, saledate, first name, m name, last name, situs address, address, city, zip code
                data: dict[str, str] = {
                    "County": "DeKalb",
                    "City": table[8],
                    "Address": table[6],
                    "Zip Code": table[9],
                    "Parcel ID": table[0],
                    "First Name": table[3],
                    "Last Name": table[5],
                    "Sale Date": table[2],
                    "Surplus Funds": table[1]
                }
                yield data

import requests, pdfplumber
from bs4 import BeautifulSoup
import bs4 #for type hints
from typing import Generator

def main() -> Generator[dict[str, str], None, None]:
#"GA - Cobb County"
    def get_main_source():
        url1: str = "https://www.cobbtax.org/property/delinquent_taxes/index.php"
        source1: str = requests.get(url1).text
        soup: bs4.BeautifulSoup = BeautifulSoup(source1, 'lxml')
        a_tag: bs4.element.Tag = soup.find('a', target="_blank", text="View Current Excess Funds List")
        url2: str = "https://cms9files.revize.com/cobbcounty/" + (a_tag.get("href"))
    
        source2: bytes = requests.get(url2).content #pdf
        file_path: str = "output/cobb.pdf"
        with open(file_path, 'wb') as file:
            file.write(source2)
    
    get_main_source()
    
    file_path: str = "output/cobb.pdf"
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            arguments = {
                "vertical_strategy": "explicit",
                "horizontal_strategy": "text",
                "explicit_vertical_lines": [40, 100, 280, 485, 580, 660, 700]
            }
            tables: list[list[str]] = page.extract_tables(arguments)[0]
            page.close()

            row: list[str]
            for row in tables:
                if row[0] != "" and row.pop() == "No": #if the row isnt empty and there is no pending claim:
                    sale_date, purchaser, owner, parcel_id, surplus_funds = row
                    data = {
                        "County": "Cobb",
                        "Pending Claim": "No",
                        "Parcel ID": (parcel_id).replace(' ', ''),
                        "Owner": owner,
                        "Purchaser": purchaser,
                        "Sale Date": sale_date,
                        "Surplus Funds": surplus_funds
                    }
                    yield data

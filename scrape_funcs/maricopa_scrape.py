import requests, pdfplumber
from bs4 import BeautifulSoup
import bs4 #for type hints
from typing import Generator
def main() -> Generator[dict[str, str], None, None]:
    def get_main_source():
        url1: str = "https://treasurer.maricopa.gov/"
        source1: str = requests.get(url1).text
        soup1: bs4.BeautifulSoup = BeautifulSoup(source1, 'lxml')
        element_list: bs4.element.ResultSet = soup1.findAll('a', target="_blank", text="Excess Proceeds")
        if element_list:
            a_tag: bs4.element.Tag = element_list.pop()
            url2: str = "https://treasurer.maricopa.gov/" + a_tag.get("href")
            source2: bytes = requests.get(url2).content
            file_path: str = "output/maricopa.pdf"
            with open(file_path, 'wb') as file:
                file.write(source2)
          
    get_main_source()
    file_path: str = "output/maricopa.pdf"
    with pdfplumber.open(file_path) as pdf:
        page: pdfplumber.page.Page
        for page in pdf.pages:
            arguments: dict[str, str|int] = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            }
            tables: list[list[str]] = page.extract_tables(arguments)[0]
            page.close()

            table: list[str]
            for table in tables[1::]: #first is table info
                trustor, deposit_date, amount_received, case_balance, civil_action_number = table
                data: dict[str, str] = {
                    "County": "Maricopa",
                    "Civil Action Number": civil_action_number,
                    "Trustor": trustor,
                    "Sale Date": deposit_date,
                    "Surplus Funds": f"${case_balance}"
                }
                yield data
main()
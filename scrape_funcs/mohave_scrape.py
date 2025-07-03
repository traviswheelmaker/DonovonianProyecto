import requests, pdfplumber
from bs4 import BeautifulSoup
from typing import Generator

def main() -> Generator[dict[str, str], None, None]:
    def get_main_source() -> None:
        url: str = "https://www.mohave.gov/media/z0njhgwu/excessproceedslist.pdf"

        source: str = requests.get(url).content
        file_path: str = "output/mohave.pdf"
        with open(file_path, 'wb') as file:
            file.write(source)
    get_main_source()
    
    file_path: str = "output/mohave.pdf"
    with pdfplumber.open(file_path) as pdf:
        z: int
        page: pdfplumber.page.Page
        for z, page in enumerate(pdf.pages):
            if z == 0:
                cropbox:  tuple[int, int, int, int] = (0, 325, 612, 792)
            else:
                cropbox: tuple[int, int, int, int] = (0, 0, 612, 792)
            cropped_area: pdfplumber.page.CroppedPage = page.crop(cropbox)

            arguments: dict[str, str] = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text"
            }
            tables: list[list[str]] = cropped_area.extract_tables(arguments)[0]#result is [tables], so we have to use [0]
            page.close()
            table: list[str]
            for table in tables:
                if len(table[3]) > 0:
                    if z:
                        case_number: str = table[0]
                        trustor: str = f"{table[1]}{table[2]}{table[3]}"
                        deposit_date: str = f"{table[4]}"
                        current_balance: str = f"{table[6]}"
                    else:
                        case_number: str = table[0]
                        trustor: str = f"{table[1]}{table[2]}"
                        deposit_date: str = f"{table[3]}"
                        current_balance: str = f"{table[5]}"
                    data: dict[str, str] = {
                        "County": "Mohave",
                        "Case Number": case_number,
                        "Trustor": trustor,
                        "Sale Date": deposit_date,
                        "Surplus Funds": current_balance
                    }
                    yield data
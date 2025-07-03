from scrape_funcs.titan import Titan
from scraper import initScrape
import re

def main() -> None:

    def inputter(phrase: str, rules: str) -> str:
        while True:
            value: str = input(phrase)
            if re.fullmatch(rules, value) != None:
                print("\n")
                return value
            else:
                print("Improper input. Please try again.")
    
    money_min: int = 0
    year_min: int = 1900
    county_input: str = ""
    counties_full: list[str] = []
    counties_included: list[str] = []

    money_rules: str = r"\d+"
    year_rules: str = r"\d{4}"
    county_keys_rules: str = r"\d+"

    ###inputs###
    print("\nWelcome!\n")

    money_min = int(inputter("Minimum dollars:   ", money_rules))
    
    year_min = int(inputter("Earliest year:   ", year_rules))

    counties_full = ["All counties"] + Titan.return_display_names()
    [print(f"{i}  -  {value}") for i, value in enumerate(counties_full)]

    county_input = inputter("County Numbers:   ", county_keys_rules)
    if "0" in county_input:
        counties_included = counties_full[1:]
    else:
        counties_included = [counties_full[int(i)] for i in county_input]

    initScrape(money_min, year_min, counties_included)
    print("Scrape completed")


if __name__ == "__main__":
    main()
import json, os, re
from typing import Generator
from collections.abc import Callable

from scrape_funcs.titan import Titan



class initScrape: 
    def __init__(self, money_min: int, year_min: int, county_list: list[str]):
        self.money_min: int = money_min
        self.year_min: int = year_min
        self.inc_county_list: list[str] = county_list

        self.surplus_funds_key: str = "Surplus Funds"
        self.date_key: str = "Sale Date"


        #we gotta delete all files in output file
        def clean() -> None:
            files: list[str] = os.listdir("output")

            file: str
            for file in files:
                if file != "__pycache__": #os doesn't let use remove pycache for some reason
                    os.remove(f"output/{file}")
        #clean()
        
        self.gen_list: list[Generator[dict[str, str], None, None] | None] = list() #will hold all generator objects from scrape funcs, holds nothing for now

        func_to_call: Callable[[], Generator[dict[str, str], None, None]] | None
        county: str
        for county in self.inc_county_list:
            if (func_to_call := Titan.func_grabber(county)) != None:
                self.safe_run(func_to_call)
        

        if self.gen_list:
            self.sort_and_save()

        
    def safe_run(self, func: Callable[[], Generator[dict[str, str], None, None]]) -> None:
        try:
            new_gen: Generator[dict[str, str], None, None] = func()
            self.gen_list.append(new_gen)
        except:
            print(f"{func.__name__} failed to return value")
    

    def sort_and_save(self) -> None:
        cleaned_info_dict: dict[int, dict[str, str]] = dict()
        global_i: int = 0

        money_pattern: re.Pattern = re.compile(r"\d+")
        date_pattern: re.Pattern = re.compile(r"^(\d+)/\d+/(\d+)")

        gen: Generator[dict[str, str], None, None]
        for gen in self.gen_list:
            row: dict[str, str]
            for row in gen:
                #we remove the commas, and slice the first and last three characters (the first is $, last are . and cents)
                money_nums: list[str] = (money_pattern.findall(row[self.surplus_funds_key]))[0: -1]
                money: int = int("".join(money_nums))

                month: int; year: int
                month, year = [int(i) for i in (date_pattern.findall(row[self.date_key]))[0]]

                if money >= int(self.money_min):
                    if year >= int(self.year_min):
                        cleaned_info_dict.update({global_i: row})
                        global_i += 1
        file_path: str = "output/data.json"
        json_file = json.dumps(cleaned_info_dict, indent=4)
        
        with open(file_path, "w") as file:
            file.write(json_file)

    
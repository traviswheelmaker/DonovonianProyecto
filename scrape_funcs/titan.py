import scrape_funcs
from collections.abc import Callable
from typing import Generator
import scrape_funcs
import scrape_funcs.cobb_scrape
import scrape_funcs.dekalb_scrape
import scrape_funcs.duval_scrape
import scrape_funcs.franklin_scrape
import scrape_funcs.mohave_scrape
import scrape_funcs.maricopa_scrape
class Titan:
    def return_display_names() -> list[str]:
        #returns names to display on ui
        county_list = [
        "FL - Duval County",
        "OH - Franklin County",
        "GA - Cobb County",
        "AZ - Mohave County",
        "AZ - Maricopa County",
        "GA - DeKalb County"
        ]
        return county_list
    
    def func_grabber(county_name: str) -> Callable[[], Generator[dict[str, str], None, None]] | None:
        match county_name:
            case "FL - Duval County":
                return scrape_funcs.duval_scrape.main
            
            case "OH - Franklin County":
                return scrape_funcs.franklin_scrape.main
            
            case "GA - Cobb County":
                return scrape_funcs.cobb_scrape.main
            
            case "AZ - Mohave County":
                return scrape_funcs.mohave_scrape.main
            
            case "AZ - Maricopa County":
                return scrape_funcs.maricopa_scrape.main
            
            case "GA - DeKalb County":
                return scrape_funcs.dekalb_scrape.main
            
            case _:
                print("Unmatched county func")
                return None
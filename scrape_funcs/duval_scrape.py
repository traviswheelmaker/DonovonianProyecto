import requests
from typing import Generator
def main() -> Generator[dict[str, str], None, None]:
    #"FL - Duval County"
    #first, we send a request for only one row to get records number
    url1: str  = f"https://taxdeed.duvalclerk.com/Home/GridSearchData?SearchType=Surplus&_search=true&nd=1748426400904&rows={1}&page=1&sidx=&sord=asc&filters=%7B%22groupOp%22%3A%22AND%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22Status%22%2C%22op%22%3A%22bw%22%2C%22data%22%3A%22SOLD%22%7D%5D%7D"
    data1: dict[str, int|dict] = requests.get(url1).json()

    #we will take that records number, and will now use that number to get all records
    row_num: int = data1["records"]
    url2: str  = f"https://taxdeed.duvalclerk.com/Home/GridSearchData?SearchType=Surplus&_search=true&nd=1748426400904&rows={row_num}&page=1&sidx=&sord=asc&filters=%7B%22groupOp%22%3A%22AND%22%2C%22rules%22%3A%5B%7B%22field%22%3A%22Status%22%2C%22op%22%3A%22bw%22%2C%22data%22%3A%22SOLD%22%7D%5D%7D"
    data2: dict[str, int|dict] = requests.get(url2).json()
    
    row: dict[str, str]
    for row in data2["rows"]:
        #all vars below are type str
        applicant, case_number, certificate, parcel_id, sale_date, status, opening_bid, high_bid, surplus_funds, owner = row["cell"]
        data: dict[str, str] = {
            "County": "Duval",
            "Case Number": case_number,
            "Parcel ID": parcel_id,
            "Certificate": certificate,
            "Owner": owner,
            "Applicant": applicant,
            "Sale Date": sale_date,
            "Surplus Funds": surplus_funds
        }
        yield data

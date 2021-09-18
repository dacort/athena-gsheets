import os
from typing import Any, Dict, List, Mapping

import pyarrow as pa
import requests

from athena.federation.athena_data_source import AthenaDataSource

API_KEY = os.getenv("GOOGLE_SHEET_API_KEY")

class GoogleSheetsDataSource(AthenaDataSource):
    """
    An Athena Data Source for Google Sheets

    Currently one sheet per data source, just for fun. :)
    """
    def __init__(self, sheet_id : str):
        super().__init__()
        self.sheet_id = sheet_id
        self.headers = get_headers(sheet_id, "All!A1:1")
        self.last_column = excel_col(len(self.headers))
    
    def databases(self) -> List[str]:
        return ["security"]
    
    def tables(self, database_name: str) -> List[str]:
        return ["0day_wild"]
    
    def columns(self, database_name: str, table_name: str) -> List[str]:
        return self.headers
    
    def schema(self, database_name: str, table_name: str) -> pa.Schema:
        return super().schema(database_name, table_name)

    def records(self, database: str, table: str, split: Mapping[str,str]) -> Dict[str,List[Any]]:
        """
        Retrieve records from a Google Sheet
        """
        sheet_rows = get_sheet_data(self.sheet_id, f"All!A2:{self.last_column}")
        # We unfortunately need to transpose the data - we should add a helper for this
        return dict(zip(self.headers, list(zip(*sheet_rows))))


def excel_col(col):
    """Covert 1-relative column number to excel-style column label."""
    quot, rem = divmod(col-1,26)
    return excel_col(quot) + chr(rem+ord('A')) if col!=0 else ''


def main():
    sheet_id = "1lkNJ0uQwbeC1ZTRrxdtuPLCIl7mlUreoKfSIgajnSyY"

    headers = get_headers(sheet_id, "All!A1:1")
    print(",".join(headers))

    sheet_range = f"All!A2:{excel_col(len(headers))}"
    print(sheet_range)
    for row in get_sheet_data(sheet_id, sheet_range):
        print(",".join(row))


def get_headers(sheet_id: str, sheet_range: str) -> list:
    """
    Retrieve the first row of data from a public Google Sheet
    """
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_range}?key={API_KEY}"
    resp = requests.get(url).json()
    values = resp.get("values", [])
    return values[0]


def get_sheet_data(sheet_id: str, sheet_range: str) -> list:
    """
    Get data from a public Google Sheet using the v4 API
    """
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_range}?key={API_KEY}"
    resp = requests.get(url).json()
    values = resp.get("values", [])
    # GSheets can return us empty rows, so we filter them out
    return [v for v in values if any(x.strip()>"" for x in v)]


if __name__ == "__main__":
    main()

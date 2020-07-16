from iexdownload.downloader import Downloader
from iexdownload.writer import CsvWriter
from iexdownload.etf import (
    commodity,
    currency,
    us_sector,
    global_sector,
    us_equity,
    global_equity,
    bond,
)
from iexcloud import set_mode, set_token

set_mode("PRODUCTION")
set_token("TOKEN")

production_writer = CsvWriter("./production")
staging_writer = CsvWriter("./staging")

download = Downloader()

holdings = [
    "KR",
    "JD",
    "KO",
    "TWTR",
    "INTU",
    "EBAY",
    "CMG",
    "LQD",
    "YUMC",
    "SQ",
    "GPRO",
    "PEP",
    "WMT",
    "MCD",
    "TEAM",
    "APRN",
    "CRM",
    "SPOT",
    "STZ",
    "GOOGL",
    "FB",
    "ONDK",
    "T",
    "KWEB",
    "KHC",
    "TPR",
    "PFE",
    "DIS",
    "TCEHY",
]


download.add_symbol(commodity)
download.add_writer(production_writer)
download.add_writer(staging_writer)

download.download_price()
download.download_dividend()
download.download_split()

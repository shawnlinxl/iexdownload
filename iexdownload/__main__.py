from iexdownload.downloader import Downloader
from iexdownload.writer import CsvWriter
from iexdownload.ticker import (
    commodity,
    currency,
    us_sector,
    global_sector,
    us_equity,
    global_equity,
    bond,
    holding,
)
from iexcloud import set_mode, set_token, set_test_token

set_mode("PRODUCTION")
set_token("TOKEN")

production_writer = CsvWriter("./production")
staging_writer = CsvWriter("./staging")

download = Downloader()


download.add_symbol(holding)
download.add_writer(production_writer)
download.add_writer(staging_writer)

download.download_price()
download.download_dividend()
download.download_split()
download.download_profile()

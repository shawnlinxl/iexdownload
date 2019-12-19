from iexdownload.downloader import Downloader
from iexdownload.writer import DBWriter

writers = [
    DBWriter(user="postgres", password="password", db="iex", port="5432"), # Production
    DBWriter(user="postgres", password="password", db="iex", port="5431"), # Staging
]

download = Downloader(symbol=['KR',
                              'JD',
                              'KO',
                              'TWTR',
                              'INTU',
                              'EBAY',
                              'CMG',
                              'LQD',
                              'YUMC',
                              'SQ',
                              'GPRO',
                              'PEP',
                              'WMT',
                              'MCD',
                              'TEAM',
                              'APRN',
                              'CRM',
                              'SPOT',
                              'STZ',
                              'GOOGL',
                              'FB',
                              'ONDK',
                              'T',
                              'KWEB',
                              'KHC',
                              'TPR',
                              'PFE',
                              'DIS',
                              'TCEHY'], db=writers)
download.download_price(time_range="5d")

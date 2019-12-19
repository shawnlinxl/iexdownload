from typing import List

from iexcloud.reference import Reference
from iexcloud.stock import Stock

from iexdownload.writer import DBWriter


class Downloader(object):

    def __init__(self, symbol: List[str] = None, db=List[DBWriter]):

        self.ref = Reference()
        self.db = db

        if symbol is None:
            self.symbol = set()
            self.stock = dict()
        else:
            if type(symbol) is not list:
                symbol = [symbol]
            self.symbol = set(symbol)
            self.stock = {key: Stock(key, output="pandas") for key in self.symbol}

    def add_symbol(self, symbol: List[str]):

        if type(symbol) is not list:
            symbol = [symbol]

        for s in symbol:
            self.symbol.add(s)
            if s not in self.stock:
                self.stock[s] = Stock(s, output="pandas")

    def download_price(self, time_range="5d") -> None:

        for stock in self.stock.values():

            for writer in self.db:
                writer.write_df(stock.get_price(time_range=time_range), table="price", pk=["date", "symbol"])

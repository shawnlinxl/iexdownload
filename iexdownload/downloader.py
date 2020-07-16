from typing import List
from iexcloud import Stock


class Downloader(object):
    def __init__(self):

        self.symbol = set()
        self.stock = dict()
        self.writer = list()

    def add_writer(self, writer):

        self.writer.append(writer)

    def add_symbol(self, symbol: List[str]):

        if type(symbol) is not list:
            symbol = [symbol]

        for s in symbol:
            self.symbol.add(s)
            if s not in self.stock:
                self.stock[s] = Stock(s, output="pandas")

    def download_price(self, time_range: str = "5d") -> None:

        for stock in self.stock.values():

            data = stock.get_price(time_range=time_range)

            if data.shape[0] > 0:
                for writer in self.writer:
                    writer.write(data, f"price/{stock.symbol}.csv")

    def download_dividend(self, time_range: str = "1m") -> None:

        for stock in self.stock.values():

            data = stock.get_dividend(time_range=time_range)

            if data.shape[0] > 0:
                for writer in self.writer:
                    writer.write(data, f"dividend/{stock.symbol}.csv")

    def download_split(self, time_range: str = "1m") -> None:

        for stock in self.stock.values():
            data = stock.get_split(time_range=time_range)

            if data.shape[0] > 0:
                for writer in self.writer:
                    writer.write(data, f"split/{stock.symbol}.csv")

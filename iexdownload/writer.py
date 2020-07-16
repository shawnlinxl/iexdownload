import os
import pandas as pd


class CsvWriter:
    def __init__(self, path: str = None):

        if path is not None:
            self.path = path
        else:
            self.path = os.getcwd()

    @staticmethod
    def create_dir_if_not_exist(path: str):

        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def write(self, df: pd.DataFrame, path: str):

        full_path = os.path.join(self.path, path)
        self.create_dir_if_not_exist(full_path)

        df.to_csv(full_path, index=False)

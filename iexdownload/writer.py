import random
from typing import List

import pandas as pd
from sqlalchemy import create_engine


class DBWriter(object):

    def __init__(self, user, password, db, host="localhost", sql_dialect="mysql", port="3306"):

        db_connectors = {"mysql": "mysql+pymysql"}
        self.con = create_engine(f"{db_connectors[sql_dialect]}://{user}:{password}@{host}:{port}/{db}")

    def write_df(self, df, table: str, pk: List[str] = []):

        try:
            df.to_sql(name=table, con=self.con, if_exists="fail", index=False)

        except ValueError:

            query_cols = f"""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = '{table}'
            """
            cols = pd.read_sql(query_cols, con=self.con)["COLUMN_NAME"].values
            pk = list(set(pk) & set(cols))
            cols = list(set(cols) - set(pk))
            temp_table = f"temp_{table}_{random.randint(0, 1e20)}"
            df.to_sql(name=temp_table, con=self.con, if_exists="fail")

            sql_update = f"""
            UPDATE {table} AS main, {temp_table} AS temp
            SET {", ".join([f"main.{col} = temp.{col}" for col in cols])}
            WHERE {" AND ".join([f"main.{key} = temp.{key}" for key in pk])}
            """
            print(sql_update)
            self.con.execute(sql_update)
            self.con.execute(f"DROP TABLE {temp_table}")


test = DBWriter(user="root", password="password", db="DW1")
tempdf = pd.read_sql("SELECT * FROM nav", con=test.con).head()
test.write_df(pd.read_sql("SELECT * FROM nav", con=test.con).head(), "test", pk=["tradeday", "account"])
tempdf["nav"][1] = 1000
test.write_df(tempdf, "test", pk=["tradeday", "account"])

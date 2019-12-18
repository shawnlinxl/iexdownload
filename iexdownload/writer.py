from typing import Dict, Set

import pandas as pd
import pymysql


class DBWriter(object):

    def __init__(self, user, password, host="localhost"):
        self.host = host
        self.username = user
        self.password = password
        self.connection = pymysql.connect(host=host, user=user, password=password)
        self.db = self.get_db(self.connection)
        self.table = {db: self.get_table(self.connection, db) for db in self.db["Database"]}

    @staticmethod
    def get_db(conn):
        query_db = "SHOW DATABASES"
        db = pd.read_sql(query_db, conn)

        return db

    @staticmethod
    def get_table(conn, db: str):
        query_table = f"""
            SELECT table_name
              FROM information_schema.tables
             WHERE table_schema = '{db}'
        """
        table = pd.read_sql(query_table, conn)

        return table

    def create_db(self, db: str):

        self.update_db()
        if db not in self.db["Database"].values:
            try:
                with self.connection.cursor() as cursor:
                    sql = f"CREATE DATABASE IF NOT EXISTS {db}"
                    cursor.execute(sql)

                self.connection.commit()

            finally:
                self.update_db()

    def create_table(self, db: str, table: str, cols: Dict, pk: Set[str]):

        self.create_db(db)
        self.update_table()

        if table not in self.table[db]["TABLE_NAME"].values:

            try:
                with self.connection.cursor() as cursor:
                    cols[key] = (f"{cols[key]} PRIMARY KEY" for key in pk)
                    create_def = ",\n".join((f"{key} {value}" for key, value in cols.items()))
                    sql = f"""
                    CREATE TABLE IF NOT EXISTS {db}.{table} (
                    {create_def}
                    );
                    """
                    cursor.execute(sql)

                self.connection.commit()

            finally:
                self.update_table()

    def update_db(self):
        self.db = self.get_db(self.connection)

    def update_table(self):
        self.update_db()
        self.table = {db: self.get_table(self.connection, db) for db in self.db["Database"]}

    def write_df(self, df, db: str, table: str):

        self.create_db(db)
        self.create_table(db, table)

        if table in self.table[db]["TABLE_NAME"].values:
            # Table already exist
            print("WOW")
        else:
            print("NO")


test = DBWriter(user="root", password="password")
print(test.db)
print(any(test.table['DW']['TABLE_NAME'].isin(["eod_attr"])))
test.write_df(df=0, db="DW", table="eod_attr")
test.write_df(df=0, db="DW1", table="eod_attr")
print(test.connection)
test.create_db("test")
test.create_table("test", "testtable", cols={"datetime": "INT", "value": "VARCHAR(100)"}, pk={"datetime"})
test.update_table()
print(test.db)
print(test.table)

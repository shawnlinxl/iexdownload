import random
from typing import List

import pandas as pd
from sqlalchemy import create_engine


class DBWriter(object):
    def __init__(
        self, user, password, db, host="localhost", sql_dialect="postgres", port="5432"
    ):

        db_connectors = {"postgres": "postgres"}
        self.engine = create_engine(
            f"{db_connectors[sql_dialect]}://{user}:{password}@{host}:{port}"
        )
        self.create_db_if_not_exist(db, self.engine)
        self.engine = create_engine(
            f"{db_connectors[sql_dialect]}://{user}:{password}@{host}:{port}/{db}"
        )

    @staticmethod
    def create_db_if_not_exist(db, engine):

        db_list = pd.read_sql("SELECT datname FROM pg_database", engine)[
            "datname"
        ].values

        if db not in db_list:
            con = engine.connect()
            con.connection.connection.set_isolation_level(0)
            con.execute(f"create database {db}")
            con.connection.connection.set_isolation_level(1)

    def write_df(self, df, table: str, pk: List[str] = []):

        try:
            df.to_sql(name=table, con=self.engine, if_exists="fail", index=False)
            set_pk = f"""
            ALTER TABLE {table}
              ADD PRIMARY KEY ({", ".join(f'"{key}"' for key in pk)})
            """
            self.engine.execute(set_pk)

        except ValueError:

            temp_table = f"temp_{table}_{random.randint(0, 1e20)}"
            df.to_sql(name=temp_table, con=self.engine, if_exists="fail", index=False)

            sql_upsert = f"""
            INSERT INTO {table} 
            SELECT * FROM {temp_table}
            ON CONFLICT ({", ".join(f'"{key}"' for key in pk)}) DO UPDATE
              SET {", ".join(f'"{col}" = excluded."{col}"' for col in set(df.columns) - set(pk))}
            """
            self.engine.execute(sql_upsert)
            self.engine.execute(f"DROP TABLE {temp_table}")

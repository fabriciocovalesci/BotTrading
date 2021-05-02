import psycopg2
from psycopg2 import Error
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')

local_env = load_dotenv(dotenv_path)


if local_env:
    POSTGRESQL_USER = os.environ.get("POSTGRESQL_USER")
    POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
    POSTGRESQL_DATABASE = os.environ.get("POSTGRESQL_DATABASE")
    POSTGRESQL_HOST = os.environ.get("POSTGRESQL_HOST")
    POSTGRESQL_PORT = os.environ.get("POSTGRESQL_PORT")


class Config:
    def __init__(self):
        self.config = {
            "postgres" : {
                "user": POSTGRESQL_USER,
                "password": POSTGRESQL_PASSWORD,
                "host": POSTGRESQL_HOST,
                "port": POSTGRESQL_PORT,
                "database": POSTGRESQL_DATABASE
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)
        try:
            self.conn = psycopg2.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()

        except (Exception, Error) as error:
            print(f"Connection error {error}")
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class Buy(Connection):
    def __init__(self):
        Connection.__init__(self)

        create_table_query_buy = '''CREATE TABLE IF NOT EXISTS Buy
            (id_buy SERIAL PRIMARY KEY,
            amount NUMERIC (10, 2),
            date_buy DATE,
            quantity INTEGER DEFAULT 0,
            order_id VARCHAR(50),
            current_price NUMERIC (10, 2),
            paired_symbol VARCHAR(50),
            symbol_base VARCHAR(50),
            id_report INTEGER,
            FOREIGN KEY(id_report) REFERENCES Reports (id_report));'''
        self.execute(create_table_query_buy)
        self.commit()


class Sell(Connection):
    def __init__(self):
        Connection.__init__(self)

        create_table_query_sell = '''CREATE TABLE IF NOT EXISTS Sell
            (id_sell SERIAL PRIMARY KEY,
            date_sell DATE,
            quantity INTEGER DEFAULT 0,
            current_price NUMERIC (10, 2),
            paired_symbol VARCHAR(50),
            symbol_base VARCHAR(50),
            amount NUMERIC ,
            id_report INTEGER,
            id_buy INTEGER,
            FOREIGN KEY(id_report) REFERENCES Reports (id_report),
            FOREIGN KEY(id_buy) REFERENCES Buy (id_buy));'''
        self.execute(create_table_query_sell)
        self.commit()

class Reports(Connection):
    def __init__(self):
        Connection.__init__(self)

        create_table_query_reports = '''CREATE TABLE IF NOT EXISTS Reports
            (id_report SERIAL PRIMARY KEY,
            amount_buy NUMERIC (10, 2) DEFAULT 0.000,
            profit INTEGER DEFAULT 0,
            amount_sell NUMERIC (10, 2) DEFAULT 0.000,
            quantity INTEGER DEFAULT 0,
            paired_symbol VARCHAR(50));'''
        self.execute(create_table_query_reports)
        self.commit()

    def insert(self, data):
        try:
            sql = "INSERT INTO Reports (amount_buy, profit, amount_sell, quantity, paired_symbol) VALUES (%s, %s, %s, %s, %s)".format(*data)
            self.execute(sql, data)
            self.commit()
        except (Exception, Error) as error:
            print(f"Error insert Reports {error}")



import psycopg2
from psycopg2 import Error
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import *
from helpers import *

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
            amount NUMERIC (10, 4),
            date_buy TIMESTAMP,
            quantity NUMERIC (10, 5),
            order_id VARCHAR(50),
            current_price NUMERIC (10, 4),
            paired_symbol VARCHAR(50),
            symbol_base VARCHAR(50),
            id_report INTEGER,
            FOREIGN KEY(id_report) REFERENCES Reports (id_report));'''
        self.execute(create_table_query_buy)
        self.commit()

    def insert_buy(self, data):
        try:
            sql = """INSERT INTO Buy (amount, date_buy, quantity ,order_id, current_price, paired_symbol, symbol_base, id_report) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""".format(*data)
            self.execute(sql, data)
            self.commit()
        except (Exception, Error) as error:
            print(f"Error insert Reports {error}")

    def select_all_buy(self):
        try:
            sql = "SELECT * FROM Buy"
            return self.query(sql)
        except (Exception, Error) as error:
            print(f"Error select all Buy {error}")

    def select_lastest_buy(self):
        try:
            sql = "SELECT * FROM Buy ORDER BY date_buy DESC LIMIT 1"
            return self.query(sql)
        except (Exception, Error) as error:
            print(f"Error select a Buy lastest {error}")
        



class Sell(Connection):
    def __init__(self):
        Connection.__init__(self)

        create_table_query_sell = '''CREATE TABLE IF NOT EXISTS Sell
            (id_sell SERIAL PRIMARY KEY,
            date_sell TIMESTAMP,
            quantity NUMERIC (10, 5),
            current_price NUMERIC (10, 4),
            paired_symbol VARCHAR(50),
            symbol_base VARCHAR(50),
            amount NUMERIC (10, 4),
            id_report INTEGER,
            id_buy INTEGER,
            FOREIGN KEY(id_report) REFERENCES Reports (id_report),
            FOREIGN KEY(id_buy) REFERENCES Buy (id_buy));'''
        self.execute(create_table_query_sell)
        self.commit()

    def insert_sell(self, data):
        try:
            sql = """INSERT INTO Sell 
                (date_sell, quantity, current_price, paired_symbol, symbol_base, amount, id_report, id_buy) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""".format(*data)
            self.execute(sql, data)
            self.commit()
        except (Exception, Error) as error:
            print(f"Error insert Sell {error}")

    def select_all_sell(self):
        try:
            sql = "SELECT * FROM Sell"
            return self.query(sql)
        except (Exception, Error) as error:
            print(f"Error select all Sell {error}")

    def select_lastest_sell(self):
        try:
            sql = "SELECT * FROM Sell ORDER BY date_sell DESC LIMIT 1"
            return self.query(sql)
        except (Exception, Error) as error:
            print(f"Error select a Sell lastest {error}")


class Reports(Connection):
    def __init__(self):
        Connection.__init__(self)

        create_table_query_reports = '''CREATE TABLE IF NOT EXISTS Reports
            (id_report SERIAL PRIMARY KEY,
            amount_buy NUMERIC (10, 4) DEFAULT 0.0000,
            profit NUMERIC (10, 2) DEFAULT 0.0,
            amount_sell NUMERIC (10, 4) DEFAULT 0.0000,
            quantity NUMERIC (10, 5),
            paired_symbol VARCHAR(50),
            date_report DATE DEFAULT CURRENT_DATE,
            status BOOLEAN DEFAULT False);'''
        self.execute(create_table_query_reports)
        self.commit()

    def insert_report(self, data):
        try:
            sql = "INSERT INTO Reports (amount_buy, profit, amount_sell, quantity, paired_symbol, date_report, status) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(*data)
            self.execute(sql, data)
            self.commit()
        except (Exception, Error) as error:
            print(f"Error insert Reports {error}")

    def select_report_lastest(self):
        try:
            sql = "SELECT * FROM Reports WHERE status = False;"
            return self.query(sql)
        except (Exception, Error) as error:
            print(f"Error select all Reports {error}")

    def update_report_sell(self, data):
        try:
            sql = """
            UPDATE reports
                SET profit = %s,
                    amount_sell = %s,
                    status = true,
                    quantity = %s,
                    date_report = CURRENT_DATE
                WHERE status = false;
            """.format(*data)
            self.execute(sql, data)
            self.commit()
        except (Exception, Error) as error:
            print(f"Error update Reports in Sell {error}")


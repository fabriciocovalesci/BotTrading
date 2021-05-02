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


try:
    connection = psycopg2.connect(user=POSTGRESQL_USER,
                                  password=POSTGRESQL_PASSWORD,
                                  host=POSTGRESQL_HOST,
                                  port=POSTGRESQL_PORT,
                                  database=POSTGRESQL_DATABASE)

    cursor = connection.cursor()


    create_table_query_sell = '''CREATE TABLE IF NOT EXISTS Sell
    (id_sell SERIAL PRIMARY KEY,
    date_sell DATE,
    quantity INTEGER DEFAULT 0,
    current_price NUMERIC (10, 2),
    paired_symbol VARCHAR(50),
    symbol_base VARCHAR(50),
    amount NUMERIC (10, 2),
    id_report INTEGER,
    id_buy INTEGER,
    FOREIGN KEY(id_report) REFERENCES Reports (id_report),
    FOREIGN KEY(id_buy) REFERENCES Buy (id_buy));'''


    create_table_query_buy = '''CREATE TABLE IF NOT EXISTS Buy
    (id_buy SERIAL PRIMARY KEY,
    amount NUMERIC (10, 2),
    date_buy DATE,
    quantity INTEGER,
    order_id VARCHAR(50),
    current_price NUMERIC (10, 2),
    paired_symbol VARCHAR(50),
    symbol_base VARCHAR(50),
    id_report INTEGER,
    FOREIGN KEY(id_report) REFERENCES Reports (id_report));'''


    create_table_query_reports = '''CREATE TABLE IF NOT EXISTS Reports
    (id_report SERIAL PRIMARY KEY,
    amount_buy NUMERIC (10, 2),
    profit INTEGER,
    amount_sell NUMERIC (10, 2),
    quantity INTEGER,
    paired_symbol VARCHAR(50));'''

    cursor.execute(create_table_query_reports)
    cursor.execute(create_table_query_buy)
    cursor.execute(create_table_query_sell)
    connection.commit()


    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

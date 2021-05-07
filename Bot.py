from binance.client import Client, BinanceAPIException
from binance.enums import *
import time as t
from datetime import datetime, timezone
import numpy as np
import math
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sendEmail import *
from helpers import *
from connect_postgresql import Buy, Sell, Reports

dotenv_path = join(dirname(__file__), '.env')

local_env = load_dotenv(dotenv_path)


if local_env:
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
else:
    API_KEY = os.environ.get("API_KEY")
    API_SECRET = os.environ.get("API_SECRET")
    GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")


client = Client(API_KEY, API_SECRET, tld='com')
symbolTicker =  'XRPUSDT'
symbolBase = 'XRP' # 
ma50 = 0
auxPrice = 0.0



# Percente For Buy
percentePriceBUY = 1.001
percentePriceStopBUY = 1.002


# Percente For Sell
percentagePriceSELL = 1.05 #1.02
percentageStopPriceSELL = 0.999 #0.992
percentagestopLimitPriceSELL = 1.02 #0.99


# object instance for DML PostgreSQL Database
Buy_DataBase =  Buy()
Sell_DataBase = Sell()
Reports_DataBase = Reports()


# decimal places
decimal_places = 4


now = datetime.now()

while True:
        
    try:
        client = Client(API_KEY, API_SECRET, tld='com')
        
        checke_symbol_price = check_balance(symbolBase, client)
        list_of_tickers = client.get_all_tickers()
            
    except BinanceAPIException as e:
        with open("Error_Bot.txt", "a") as myfile:
            SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
            myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 1 ! \n")
        client = Client(API_KEY, API_SECRET, tld='com')
        print(f"status {e.status_code}")
        print(f'Message {e.message}')
        continue

    symbolPrice_current = get_price_current(list_of_tickers, symbolTicker)
    price_current_XRPUSDT = (symbolPrice_current*float(checke_symbol_price['quantity']))

    if len(Reports_DataBase.select_report_lastest()) != 0 and checke_symbol_price['status'] == True and round(float(price_current_XRPUSDT), decimal_places) >= 10.50:

        t.sleep(15)
        
        symbolPriceSale = get_price_current(list_of_tickers, symbolTicker)

        dict_info = get_priceBuy_Quantity(Reports_DataBase.select_report_lastest())

        if dict_info['price_buy'] == None and dict_info['quantity'] == None:
            print('Error in {dict_info}')

        quantitySell = round_down(dict_info['quantity'])
        priceBuyCompare = float(dict_info['price_buy'])

        show_await(symbolTicker, priceBuyCompare, symbolPriceSale, quantitySell, percentagePriceSELL)

        if signal_for_sell(percentagePriceSELL, list_of_tickers, symbolTicker, priceBuyCompare):
            print('\t\t____Starting Sale____')
            t.sleep(20)
            
            try:
                dict_info = get_priceBuy_Quantity(Reports_DataBase.select_report_lastest())
                return_sell = STARTING_SALE(symbolTicker, symbolBase, client, percentagePriceSELL, percentageStopPriceSELL, percentagestopLimitPriceSELL, dict_info)
                
                price_buy = float(dict_info['price_buy'])
                quantitySell = float(return_sell['quantity'])
                quantityBuy_profit = float(dict_info['quantity'])
                priceSell = float(return_sell['priceSell'])

                profit = round(float(abs((priceSell*quantitySell) - (price_buy*quantityBuy_profit))), decimal_places)

                id_report = getId_data_base(Reports_DataBase.select_report_lastest())

                id_buy = 0
                list_buy = Buy_DataBase.select_lastest_buy()
                for index in list_buy:
                    id_buy = index[0]

                quantity_sell_update_reports = float(quantitySell)
                update_query = (profit, priceSell, quantity_sell_update_reports)
                Reports_DataBase.update_report_sell(update_query)

                t.sleep(5)
                list_of_tickers = client.get_all_tickers()
                current_price_sell = get_price_current(list_of_tickers, symbolTicker)
                date_sell = datetime.now(timezone.utc)
                order_sell_tuple = (date_sell, quantitySell, current_price_sell, symbolTicker, symbolBase, priceSell, id_report, id_buy)
                Sell_DataBase.insert_sell(order_sell_tuple)
                SendEmailSell(return_sell, str(now.strftime("%d-%m-%y %H:%M:%S")))

                t.sleep(15)
            except BinanceAPIException as e:
                with open("Error_Bot.txt", "a") as myfile:
                    SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                    myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
                client = Client(API_KEY, API_SECRET, tld='com')
                continue
            
    elif float(checke_symbol_price['quantity']) < 3.00:
        print(f"No account balance {checke_symbol_price['quantity']}")
        t.sleep(15)
        
            
        get_price = client.get_asset_balance(asset=symbolBase)
        
        symbolPrice = get_price_current(list_of_tickers, symbolTicker)
                    
        print(f"Current value of {symbolTicker} - {symbolPrice}")
            
        ma50 = calculate_ma50(symbolTicker, client)
        print('ma50 ', round(ma50, decimal_places))
        print('Tendencia ', tendencia_ma50_4hs_15minCandles(symbolTicker, client))
        if (ma50 == 0): continue
        
        show_updated_prices(symbolTicker, ma50, symbolPrice)
        
        try:
            orders = client.get_open_orders(symbol=symbolTicker)
        except BinanceAPIException as e:
            with open("Error_Bot.txt", "a") as myfile:
                SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 1 ! \n")
            client = Client(API_KEY, API_SECRET, tld='com')
            print(f"status {e.status_code}")
            print(f'Message {e.message}')
            continue
        
        if (len(orders) != 0):
            print("There is Open Orders")
            t.sleep(20)
            continue
        if (not tendencia_ma50_4hs_15minCandles(symbolTicker, client)):
            print("Decreasing")
            t.sleep(20)
            continue
        else:
            print("Creasing")

        if ( symbolPrice < ma50*0.999 ):
            print("DINAMIC_BUY")
            
            try:
                client = Client(API_KEY, API_SECRET, tld='com')
                return_buy = Dinamic_Buy(symbolTicker, symbolBase, client, percentePriceBUY, percentePriceStopBUY)

                symbolPrice = float(return_buy['amount_buy'])
                quantity_buy_insert = float(return_buy['quantity'])
                
                report_buy_db = (symbolPrice, 0.0, 0.0, quantity_buy_insert, symbolTicker, datetime.now(), False)
                Reports_DataBase.insert_report(report_buy_db)

                id_report = getId_data_base(Reports_DataBase.select_report_lastest()) 

                date_buy = datetime.now(timezone.utc)
                order_id = return_buy['order_id']
                buy_tuple_db = (symbolPrice, date_buy, quantity_buy_insert ,order_id, symbolPrice, symbolTicker, symbolBase, id_report)
                Buy_DataBase.insert_buy(buy_tuple_db)
                SendEmailBuy(symbolPrice, str(now.strftime("%d-%m-%y %H:%M:%S")))

                t.sleep(20)

                if len(Reports_DataBase.select_report_lastest()) != 0:

                    reports_lastest = Reports_DataBase.select_report_lastest()
                    priceCompare = 0.0
                    for item in reports_lastest:
                        priceCompare = float(item[1])

                    list_of_tickers = client.get_all_tickers()

                    if signal_for_sell(percentagePriceSELL, list_of_tickers, symbolTicker, priceCompare):
                        print('____ Signal for Sale ____')
                        t.sleep(10)
            
                        try:
                            dict_info = get_priceBuy_Quantity(Reports_DataBase.select_report_lastest())
                            return_sell = STARTING_SALE(symbolTicker, symbolBase, client, percentagePriceSELL, percentageStopPriceSELL, percentagestopLimitPriceSELL, dict_info)

                            price_buy = float(dict_info['price_buy'])
                            quantitySell = int(return_sell['quantity'])
                            priceSell = float(return_sell['priceSell'])

                            profit = round(float(abs((priceSell*quantitySell) - (price_buy*dict_info['quantity']))), decimal_places)

                            id_report = getId_data_base(Reports_DataBase.select_report_lastest())

                            id_buy = 0
                            list_buy = Buy_DataBase.select_lastest_buy()
                            for index in list_buy:
                                id_buy = index[0]

                            quantity_sell_update_reports = float(quantitySell)
                            update_query = (profit, priceSell, quantity_sell_update_reports)
                            Reports_DataBase.update_report_sell(update_query)

                            t.sleep(5)
                            list_of_tickers = client.get_all_tickers()
                            current_price_sell = get_price_current(list_of_tickers, symbolTicker)
                            date_sell = datetime.now(timezone.utc)
                            order_sell_tuple = (date_sell, quantitySell, current_price_sell, symbolTicker, symbolBase, priceSell, id_report, id_buy)
                            Sell_DataBase.insert_sell(order_sell_tuple)
                            SendEmailSell(return_sell, str(now.strftime("%d-%m-%y %H:%M:%S")))

                            t.sleep(15)
                        except BinanceAPIException as e:
                            with open("Error_Bot.txt", "a") as myfile:
                                SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                                myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
                            client = Client(API_KEY, API_SECRET, tld='com')
                            continue

                t.sleep(10)

            except BinanceAPIException as e:
                with open("Error_Bot.txt", "a") as myfile:
                    SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                    myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
                client = Client(API_KEY, API_SECRET, tld='com')
                print(e)
                orders = client.get_open_orders(symbol=symbolTicker)
                if (len(orders)>0):
                    result = client.cancel_order(
                        symbol=symbolTicker,
                        orderId=orders[0].get('orderId'))

                continue




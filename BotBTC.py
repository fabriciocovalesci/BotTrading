from binance.client import Client, BinanceAPIException
from binance.enums import *
import time as t
from datetime import datetime, timezone
import numpy as np
import math
import os
import satoshi
from os.path import join, dirname
from dotenv import load_dotenv
from helpers_btc import *
from Connect_PostgreSQL_BTC import Buy, Sell, Reports
from Email import Gmail

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
symbolTicker = 'BTCUSDT'
symbolBase = 'BTC'

ma50 = 0
auxPrice = 0.0

amount_buy_usdt_to_btc = 50.00

# Percente For Buy
percentePriceBUY = 1.0055
percentePriceStopBUY = 1.005

# Percente For Sell
percentagePriceSELL = 1.05
# percentageStopPriceSELL = 0.999 #0.992
# percentagestopLimitPriceSELL = 1.02 #0.99 

# object instance for DML PostgreSQL Database
Buy_DataBase =  Buy()
Sell_DataBase = Sell()
Reports_DataBase = Reports()

# object instance for send Email
Send_Email = Gmail(GMAIL_EMAIL, GMAIL_PASSWORD)

# decimal places
decimal_places = 6

now = datetime.now()

while True:
        
    try:
        client = Client(API_KEY, API_SECRET, tld='com')
        
        checke_symbol_price = check_balance(symbolBase, client)
        list_of_tickers = client.get_all_tickers()
            
    except BinanceAPIException as e:
        with open("Error_Bot.txt", "a") as myfile:
            myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 1 ! \n")
        client = Client(API_KEY, API_SECRET, tld='com')
        print(f"status {e.status_code}")
        print(f'Message {e.message}')
        continue

    symbolPrice_current = get_price_current(list_of_tickers, symbolTicker)
    price_current_BTCUSDT = (symbolPrice_current*float(checke_symbol_price['quantity']))

    value_usd_current = satoshi.to_fiat(float(checke_symbol_price['quantity']) * 100000000, fiat='USD')

    if len(Reports_DataBase.select_report_lastest()) != 0 and checke_symbol_price['status'] == True and round(float(price_current_BTCUSDT), decimal_places) >= 10.50:

        t.sleep(15)

        try:
            symbolPriceSale = get_price_current(list_of_tickers, symbolTicker)

            dict_info = get_priceBuy_Quantity(Reports_DataBase.select_report_lastest())

            if dict_info['price_buy'] == None and dict_info['quantity'] == None:
                print('Error in {dict_info}')

            quantitySell = round_down(dict_info['quantity'])
            priceBuyCompare = float(dict_info['price_buy'])

            show_await(symbolTicker, priceBuyCompare, symbolPriceSale, quantitySell, percentagePriceSELL)

        except BinanceAPIException as e:
            with open("Error_Bot.txt", "a") as myfile:
                myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Error in await price ! \n")
            client = Client(API_KEY, API_SECRET, tld='com')
            continue

        if signal_for_sell(percentagePriceSELL, list_of_tickers, symbolTicker, priceBuyCompare):
            print('\t\t____Starting Sale____')
            
            try:
                client = Client(API_KEY, API_SECRET, tld='com')
                dict_info = get_priceBuy_Quantity(Reports_DataBase.select_report_lastest())

                quantity_sell_btc = quantity_bitcoin(symbolTicker, client, float(dict_info['quantity']))
               
                return_sell = SELL_MARKET(symbolTicker, quantity_sell_btc, client)

                price_buy = float(dict_info['price_buy'])
                quantitySell = float(return_sell['executedQty'])

                priceSell = float(return_sell['fills'][0]['price'])

                profit = round(float(abs((priceSell*quantitySell) - (price_buy*quantity_sell_btc))), 2)

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

                t.sleep(3)
                
                body_email_for_sell = body_email_sell(symbolTicker=symbolTicker, price_current=current_price_sell, price_buy=price_buy, price_sell=priceSell, profit=profit, quantity_sell=quantitySell)

                Send_Email.send_email("Success Sell", body_email_for_sell)

                t.sleep(15)
            except BinanceAPIException as e:
                with open("Error_Bot.txt", "a") as myfile:
                    myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
                client = Client(API_KEY, API_SECRET, tld='com')
                continue

    elif (value_usd_current < 12.00):
        print(f"No account balance {value_usd_current} USDT")
        
        t.sleep(15)
        
        get_price = client.get_asset_balance(asset=symbolBase)
        
        symbolPrice = get_price_current(list_of_tickers, symbolTicker)
                    
        print(f"Current value of {symbolTicker} - {symbolPrice}")
            
        ma50 = calculate_ma50(symbolTicker, client)
        print('Tendencia ', tendencia_ma50_4hs_15minCandles(symbolTicker, client))
        if (ma50 == 0): continue
        
        show_updated_prices(symbolTicker, ma50, symbolPrice)
        
        try:
            orders = client.get_open_orders(symbol=symbolTicker)
        except BinanceAPIException as e:
            with open("Error_Bot.txt", "a") as myfile:
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

        if ( symbolPrice < ma50*0.995 ):
            print("____ STARTING BITCOIN PURCHASE ____")
            
            try:
                client = Client(API_KEY, API_SECRET, tld='com')

                quantity_buy_bitcoin = quantity_bitcoin(symbolTicker, client, amount_buy_usdt_to_btc)
                return_buy = market_buy(client, symbolTicker, quantity_buy_bitcoin)

                price_bitcoin_buy = float(return_buy['fills'][0]['price'])
                
                value_usdt_buy = float(quantity_buy_bitcoin) * price_bitcoin_buy

                report_buy_db = (price_bitcoin_buy, 0.0, 0.0, value_usdt_buy, symbolTicker, datetime.now(), False)
                Reports_DataBase.insert_report(report_buy_db)

                id_report = getId_data_base(Reports_DataBase.select_report_lastest()) 

                date_buy = datetime.now(timezone.utc)
                order_id = return_buy['orderId']


                buy_tuple_db = (price_bitcoin_buy, date_buy, value_usdt_buy ,order_id, price_bitcoin_buy, symbolTicker, symbolBase, id_report)
                Buy_DataBase.insert_buy(buy_tuple_db)

                t.sleep(3)

                body_email_for_buy = body_email_buy(symbolTicker=symbolTicker, price_current=price_bitcoin_buy, price_buy=price_bitcoin_buy, percentagePriceSELL=percentagePriceSELL, quantity_buy=quantity_buy_bitcoin)

                Send_Email.send_email("Success Buy", body_email_for_buy)

                t.sleep(20)

            except BinanceAPIException as e:
                with open("Error_Bot.txt", "a") as myfile:
                    myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
                client = Client(API_KEY, API_SECRET, tld='com')
                print(e)
                orders = client.get_open_orders(symbol=symbolTicker)
                if (len(orders)>0):
                    result = client.cancel_order(
                        symbol=symbolTicker,
                        orderId=orders[0].get('orderId'))

                continue
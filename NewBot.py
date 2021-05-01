from binance.client import Client, BinanceAPIException
from binance.enums import *
import time
from datetime import datetime
import numpy as np
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sendEmail import *
from helpers import *

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
symbolTicker = 'XRPUSDT'
symbolBase = 'XRP'
symbolPrice = 0
priceBuy = 0
ma50 = 0
auxPrice = 0.0
priceCompare = 1.5999


# Percente For Buy
percentePriceBUY = 1.001
percentePriceStopBUY = 1.002


# Percente For Sell
percentagePriceSELL = 1.02
percentageStopPriceSELL = 0.992
percentagestopLimitPriceSELL = 0.99


quantitySell = 0

now = datetime.now()

while True:
        
    try:
        client = Client(API_KEY, API_SECRET, tld='com')
        
        checke_symbol_price = check_balance(symbolBase, client)
        list_of_tickers = client.get_all_tickers()
            
    except BinanceAPIException as e:
        print(f'An exception occurred {e}')
        print(f"status {e.status_code}")
        print(f'Message {e.message}')
        continue

    symbolPrice_current = get_price_current(list_of_tickers, symbolTicker)
    price_current_XRPUSDT = (symbolPrice_current*float(checke_symbol_price['price']))
    if checke_symbol_price['status'] == True and round(float(price_current_XRPUSDT), 4) >= 10.50:
        print(f"Account Balance .... {round(float(price_current_XRPUSDT), 4)} USDT")
        print(f"The Amount {int(checke_symbol_price['price'])} XRP for sale")
        time.sleep(15)
        
        if signal_for_sell(percentagePriceSELL, list_of_tickers, symbolTicker, priceCompare):
            print('\t\t____Confirmed Sale____')
            
            priceSell = format_Price_decimal_percente(str(symbolPrice), percentagePriceSELL, 4)
            stopPriceSell = format_Price_decimal_percente(str(symbolPrice), percentageStopPriceSELL, 4)
            stopLimitPriceSell = format_Price_decimal_percente(str(symbolPrice), percentagestopLimitPriceSELL, 4)
            quantitysell = int(checke_symbol_price['price'])
            
            orderOCO = sell_order_OCO(client, symbolTicker, quantitysell, priceSell, stopPriceSell, stopLimitPriceSell)
            
            SendEmailSell(orderOCO, str(now.strftime("%d-%m-%y %H:%M:%S")))
            time.sleep(10)
        continue
            
            
    elif float(checke_symbol_price['price']) < 3.00:
        print(f"No account balance {checke_symbol_price['price']}")
        time.sleep(5)
            
        get_price = client.get_asset_balance(asset=symbolBase)
        
        symbolPrice = get_price_current(list_of_tickers, symbolTicker)
                    
        print(f"Current value of {symbolTicker} - {symbolPrice}")
            
        ma50 = calculate_ma50(symbolTicker, client)
        print('ma50 ', round(ma50, 4))
        print('Tendencia ', tendencia_ma50_4hs_15minCandles(symbolTicker, client))
        if (ma50 == 0): continue
        
        show_updated_prices(symbolTicker, ma50, symbolPrice)
        
        try:
            orders = client.get_open_orders(symbol=symbolTicker)
        except BinanceAPIException as e:
            print(f"status {e.status_code}")
            print(f'Message {e.message}')
            client = Client(API_KEY, API_SECRET, tld='com')
            continue
        
        if (len(orders) != 0):
            print("There is Open Orders")
            time.sleep(20)
            continue
        if (not tendencia_ma50_4hs_15minCandles(symbolTicker, client)):
            print("Decreasing")
            time.sleep(20)
            continue
        else:
            print("Creasing")

        if ( symbolPrice < ma50*0.999 ):
            print("DINAMIC_BUY")
            
            try:
                client = Client(API_KEY, API_SECRET, tld='com')
                symbolPrice = Dinamic_Buy(symbolTicker, symbolBase, client, percentePriceBUY, percentePriceStopBUY)
                SendEmailBuy(symbolPrice, str(now.strftime("%d-%m-%y %H:%M:%S")))

                time.sleep(20)
                
                priceSell = format_Price_decimal_percente(symbolPrice, percentagePriceSELL, 4)
                stopPriceSell = format_Price_decimal_percente(symbolPrice, percentageStopPriceSELL, 4)
                stopLimitPriceSell = format_Price_decimal_percente(symbolPrice, percentagestopLimitPriceSELL, 4)

                orderOCO = sell_order_OCO(client, symbolTicker, quantitySell, priceSell, stopPriceSell, stopLimitPriceSell)
                SendEmailSell(orderOCO, str(now.strftime("%d-%m-%y %H:%M:%S")))

                time.sleep(20)

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




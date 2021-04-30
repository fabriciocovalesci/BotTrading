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
symbolTicker = 'XRPUSDT' # 'DGBUSDT'
symbolBase = 'XRP' #'DGB'
symbolPrice = 0
priceBuy = 0
ma50 = 0
auxPrice = 0.0
priceCompare = 1.3375


# Percente For Buy
percentePriceBUY = 1.002
percentePriceStopBUY = 1.003


# Percente For Sell
percentagePriceSELL = 1.080
percentageStopPriceSELL = 1.048
percentagestopLimitPriceSELL = 1.050

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

    if checke_symbol_price['status'] == True and float(checke_symbol_price['price']) >= 10.00:
        time.sleep(15)
        print(f"status {checke_symbol_price['price']}")
        if signal_for_sell(percentagePriceSELL, list_of_tickers, symbolTicker, priceCompare):
            print('venda confirmada......')
        
            # priceSell = format_Price_decimal_percente(str(symbolPrice), percentagePriceSELL, 4)
            # stopPriceSell = format_Price_decimal_percente(str(symbolPrice), percentageStopPriceSELL, 4)
            # stopLimitPriceSell = format_Price_decimal_percente(str(symbolPrice), percentagestopLimitPriceSELL, 4)

            # orderOCO = sell_order_OCO(client, symbolTicker, quantitySell, priceSell, stopPriceSell, stopLimitPriceSell)
            # SendEmailSell()
        continue
            
            
    elif float(checke_symbol_price['price']) < 1.00:
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

        if ( symbolPrice < ma50*0.99 ):
            print("DINAMIC_BUY")
            
            try:
            
                priceBuy = format_Price_decimal_percente(symbolPrice, percentePriceBUY, 4)
                stopPriceBuy = format_Price_decimal_percente(symbolPrice, percentePriceStopBUY, 4)
                quantityBuy = calculate_price_buy(symbolTicker, client)
                quantitySell = quantityBuy
                
                print('=========================================')
                print('priceBuy ', priceBuy)
                print('stopPriceBuy ', stopPriceBuy)
                print('quantityBuy ', quantityBuy)
                print('quantitySell ', quantitySell)
                print('=========================================')

                buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)
                priceCompare = priceBuy
                SendEmailBuy()
                print("orderStatus(buyOrder) ", orderStatus(buyOrder, client))

                auxPrice = symbolPrice
                time.sleep(3)
                
                while orderStatus(buyOrder, client)=='NEW':
                    client = Client(API_KEY, API_SECRET, tld='com')
                    # BEGIN GET PRICE
                    try:
                        list_of_tickers = client.get_all_tickers()
                    except BinanceAPIException as e:
                        with open("Error_Bot.txt", "a") as myfile:
                            SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                            myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 2 ! \n")
                        client = Client(API_KEY, API_SECRET, tld='com')
                        continue
                    
                    symbolPrice = get_price_current(list_of_tickers, symbolTicker)
                    # END GET PRICE

                    if (symbolPrice < auxPrice):

                        try:
                            result = client.cancel_order(
                                symbol=symbolTicker,
                                orderId=buyOrder.get('orderId'))

                            time.sleep(3)
                        except BinanceAPIException as e:
                            with open("Error_Bot.txt", "a") as myfile:
                                SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                                myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ "Error Canceling Oops 4 ! \n")
                            break

                        priceBuy = format_Price_decimal_percente(symbolPrice, percentePriceBUY, 4)
                        stopPriceBuy = format_Price_decimal_percente(symbolPrice, percentePriceStopBUY, 4)      
                        quantityBuy = calculate_price_buy(symbolTicker, client)
                        quantitySell = quantityBuy

                        buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)
                        auxPrice = symbolPrice
                        priceCompare = priceBuy
                        SendEmailBuy()
                        time.sleep(1)

                time.sleep(10)
                
                priceSell = format_Price_decimal_percente(symbolPrice, percentagePriceSELL, 4)
                stopPriceSell = format_Price_decimal_percente(symbolPrice, percentageStopPriceSELL, 4)
                stopLimitPriceSell = format_Price_decimal_percente(symbolPrice, percentagestopLimitPriceSELL, 4)

                orderOCO = sell_order_OCO(client, symbolTicker, quantitySell, priceSell, stopPriceSell, stopLimitPriceSell)
                SendEmailSell()

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




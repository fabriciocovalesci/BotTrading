from binance.client import Client
from binance.enums import *
import time
import math
from datetime import datetime
import numpy as np
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sendEmail import *

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
symbolTicker = 'NANOUSDT'
symbolPrice = 0
ma50 = 0
auxPrice = 0.0


# Percente For Buy
percentePriceBUY = 1.0055
percentePriceStopBUY =  1.005


# Percente For Sell
percentagePriceSELL = 1.080
percentageStopPriceSELL = 1.048
percentagestopLimitPriceSELL = 1.050

quantitySell = 0

now = datetime.now()


def formatForPrice(priceToFormat, percente):
    return '{:.8f}'.format(round(float(priceToFormat*percente),8))



def calculate_price_buy(crypto):
    """
    This function receives a symbol as a parameter, and returns the minimum amount to 10.00 USDT
    
    :params crypto:
    
    :type crypto: str
    
    returns the minimum quantity to Buy
    """
    current_price = client.get_symbol_ticker(symbol=crypto)
    get_price = float(current_price['price'])
    
    if get_price >= 10.0 and get_price <= 20.0:
        print(f'Current price bigger then 10, price {get_price} USDT | Buy quantity 1')
        return 1
    elif get_price <= 10.0:
        quantity = 1
        while True:
            quantity_current = get_price * quantity
            if quantity_current < 10.0:
                quantity +=1
                continue
            break
        print(f'Current price less than 10, price unit {get_price} -- price buy {get_price*quantity} USDT | Buy quantity {quantity}')
        return quantity
    

def orderStatus(orderToCkeck):
    try:
        status = client.get_order(
            symbol = symbolTicker,
            orderId = orderToCkeck.get('orderId')
        )
        return status.get('status')
    except Exception as e:
        print(e)
        return 7

def _tendencia_ma50_4hs_15minCandles_():
    x = []
    y = []
    sum = 0
    ma50_i = 0

    time.sleep(1)

    resp = False

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "18 hour ago UTC")

    if (len(klines) != 72):
        return False
    for i in range(56,72):
        for j in range(i-50,i):
            sum = sum + float(klines[j][4])
        ma50_i = round(sum / 50,8)
        sum = 0
        x.append(i)
        y.append(float(ma50_i))

    modelo = np.polyfit(x, y, 1)

    if (modelo[0]>0):
        resp = True

    return resp

def _ma50_():
    ma50_local = 0
    sum = 0

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")

    if (len(klines) == 60):

        for i in range(10,60):
            sum = sum + float(klines[i][4])

        ma50_local = sum / 50

    return ma50_local

while 1:

    time.sleep(3)
    sum = 0

    # BEGIN GET PRICE
    try:
        list_of_tickers = client.get_all_tickers()
    except Exception as e:
        with open("ADABTC_scalper.txt", "a") as myfile:
            SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
            myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 1 ! \n")
        client = Client(API_KEY, API_SECRET, tld='com')
        continue

    for tick_2 in list_of_tickers:
        if tick_2['symbol'] == symbolTicker:
            symbolPrice = float(tick_2['price'])
    # END GET PRICE

    ma50 = _ma50_()
    if (ma50 == 0): continue

    print("********** " + symbolTicker + " **********")
    print(" ActualMA50: "  + str(round(ma50,8)))
    print("ActualPrice: " + str(round(symbolPrice,8)))
    print(" PriceToBuy: "  + str(round(ma50*0.99,8)))
    print("----------------------")

    try:
        orders = client.get_open_orders(symbol=symbolTicker)
    except Exception as e:
        print(e)
        client = Client(API_KEY, API_SECRET, tld='com')
        continue

    if (len(orders) != 0):
        print("There is Open Orders")
        time.sleep(20)
        continue
    if (not _tendencia_ma50_4hs_15minCandles_()):
        print("Decreasing")
        time.sleep(20)
        continue
    else:
        print("Creasing")

    if ( symbolPrice < ma50*0.99 ):
        print("DINAMIC_BUY")

        try:
            
            priceBuy = formatForPrice(symbolPrice, percentePriceBUY)
            stopPriceBuy = formatForPrice(symbolPrice, percentePriceStopBUY)
            quantityBuy = calculate_price_buy(symbolTicker)
            quantitySell = quantityBuy

            buyOrder = client.create_order(
                        symbol=symbolTicker,
                        side='BUY',
                        type='STOP_LOSS_LIMIT',
                        quantity=quantityBuy,
                        price=priceBuy,
                        stopPrice=stopPriceBuy,
                        timeInForce='GTC')
            SendEmailBuy(priceBuy, buyOrder)

            auxPrice = symbolPrice
            time.sleep(3)
            while orderStatus(buyOrder)=='NEW':

                # BEGIN GET PRICE
                try:
                    list_of_tickers = client.get_all_tickers()
                except Exception as e:
                    with open("ADABTC_scalper.txt", "a") as myfile:
                        SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                        myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 2 ! \n")
                    client = Client(API_KEY, API_SECRET, tld='com')
                    continue

                for tick_2 in list_of_tickers:
                    if tick_2['symbol'] == symbolTicker:
                        symbolPrice = float(tick_2['price'])
                # END GET PRICE

                if (symbolPrice < auxPrice):

                    try:
                        result = client.cancel_order(
                            symbol=symbolTicker,
                            orderId=buyOrder.get('orderId'))

                        time.sleep(3)
                    except Exception as e:
                        with open("ADABTC_scalper.txt", "a") as myfile:
                            SendEmailERROR(e, str(now.strftime("%d-%m-%y %H:%M:%S")))
                            myfile.write(str(now.strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ "Error Canceling Oops 4 ! \n")
                        break

                    priceBuy = formatForPrice(symbolPrice, percentePriceBUY)
                    stopPriceBuy = formatForPrice(symbolPrice, percentePriceStopBUY)
                    quantityBuy = calculate_price_buy(symbolTicker)
                    quantitySell = quantityBuy

                    buyOrder = client.create_order(
                                symbol=symbolTicker,
                                side='BUY',
                                type='STOP_LOSS_LIMIT',
                                quantity=250,
                                price=priceBuy,
                                stopPrice=stopPriceBuy,
                                timeInForce='GTC')
                    auxPrice = symbolPrice
                    SendEmailBuy(priceBuy, buyOrder)
                    time.sleep(1)

            time.sleep(10)
            
            priceSell = formatForPrice(symbolPrice, percentagePriceSELL)
            stopPriceSell = formatForPrice(symbolPrice, percentageStopPriceSELL)
            stopLimitPriceSell = formatForPrice(symbolPrice, percentagestopLimitPriceSELL)

            orderOCO = client.order_oco_sell(
                        symbol = symbolTicker,
                        quantity = quantitySell,
                        price = priceSell,
                        stopPrice = stopPriceSell,
                        stopLimitPrice =stopLimitPriceSell,
                        stopLimitTimeInForce = 'GTC'
                    )
            SendEmailSell(priceSell, orderOCO)

            time.sleep(20)

        except Exception as e:
            with open("ADABTC_scalper.txt", "a") as myfile:
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
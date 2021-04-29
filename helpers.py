from binance.client import Client
from binance.enums import *
import time
import numpy as np


def calculate_ma50(symbolTicker, client):
    ma50_local = 0
    sum = 0

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")

    if (len(klines) == 60):

        for i in range(10,60):
            sum = sum + float(klines[i][4])

        ma50_local = sum / 50

    return ma50_local


def orderStatus(orderToCkeck, client):
    try:
        status = client.get_order(
            symbol = symbolTicker,
            orderId = orderToCkeck.get('orderId')
        )
        return status.get('status')
    except Exception as e:
        print(e)
        return 7

def tendencia_ma50_4hs_15minCandles(symbolTicker, client):
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


def calculate_price_buy(crypto, client):
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
    
    
def format_Price_decimal_percente(priceToFormat, percente, decimal) -> float:
    """
    This function returns a price formatted to 8 decimal places
    
    :params priceToFormat:
    :params percente:
    
    :type priceToFormat: str
    :type percente: float
    
    returns a formatted price, already with a percentage added
    """
    price = float(priceToFormat)
    result = price*percente
    return f"{round(float(result),decimal)}"


def check_balance(symbol, client):
    """
    This function returns a Boolean value
    
    :params symbol:
    
    :type symbol: str
    
    returns a bool, True if there is a symbol in the wallet and False if there is no symbol
    """
    balance = client.get_asset_balance(asset=symbol)
    get_price = float(balance['free'])
    if get_price == 0.0:
        return {"status": False, "price": get_price}
    return {"status": True, "price": get_price}



def buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy, stopPriceBuy):
    """
    This function returns a buy order with stop limit
    
    :params client:
    :params symbolTicker:
    :params quantityBuy:
    :params priceBuy:
    :params stopPriceBuy:
    
    :type client: Binance client instance
    :type symbolTicker: str
    :type quantityBuy: int
    :type priceBuy: str
    :type stopPriceBuy: str
    
    returns a dict with orderId to buy
    """
    buyOrder = client.create_order(
        symbol=symbolTicker,
        side='BUY',
        type='STOP_LOSS_LIMIT',
        quantity=quantityBuy,
        price=priceBuy,
        stopPrice=stopPriceBuy,
        timeInForce='GTC')
    return buyOrder              


def sell_order_OCO(client, symbolTicker, quantitySell, priceSell, stopPriceSell, stopLimitPriceSell):
    """
    This function returns a sell order with stop limit
    
    :params client:
    :params symbolTicker:
    :params quantitySell:
    :params priceSell:
    :params stopPriceSell:
    :params stopLimitPriceSell:
    
    :type client: Binance client instance
    :type symbolTicker: str
    :type quantitySell: int
    :type priceSell: str
    :type stopPriceSell: str
    :type stopLimitPriceSell: str
    
    returns a dict with orderId to sell
    """
    
    orderOCO = client.order_oco_sell(
        symbol = symbolTicker,
        quantity = quantitySell,
        price = priceSell,
        stopPrice = stopPriceSell,
        stopLimitPrice =stopLimitPriceSell,
        stopLimitTimeInForce = 'GTC')
    return orderOCO


def get_price_ticker(symbol, client):
  """
  This function returns the price of the symbol
  
  :params symbol:
  :params client:
  
  :type symbol: str
  :type client: Binance instance client
  
  return a price in float
  """
  list_of_tickers = client.get_all_tickers()
  for tick in list_of_tickers:
    if tick['symbol'] == symbol:
      symbolPrice = float(tick['price'])
      break
  return symbolPrice



def show_updated_prices(symbolTicker,ma50, symbolPrice):
    """
    This function displays prices
    
    :params symbolTicker:
    :params ma50:
    :params symbolPrice:
    
    :type symbolTicker: str
    :type ma50: float
    :type symbolPrice: str
    """
    print("********** " + symbolTicker + " **********")
    print(" ActualMA50: "  + str(round(ma50,4)))
    print("ActualPrice: " + str(round(symbolPrice,4)))
    print(" PriceToBuy: "  + str(round(ma50*0.99,4)))
    print("----------------------")
    

def formatForPriceDecimal(priceToFormat, decimal):
    return  f"{round(float(priceToFormat), decimal)}"
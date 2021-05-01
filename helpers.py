from binance.client import Client, BinanceAPIException
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
    
    if get_price >= 10.50 and get_price <= 20.0:
        print(f'Current price bigger then 10, price {get_price} USDT | Buy quantity 1')
        return 1
    elif get_price <= 10.50:
        quantity = 1
        while True:
            quantity_current = get_price * quantity
            if quantity_current < 10.50:
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
    

def formatForPriceDecimal(priceToFormat: str, decimal: float) -> float:
    return  f"{round(float(priceToFormat), decimal)}"


def signal_for_sell(percenteSell: float, list_all_tickers: list, symbolTicker: str, priceCompare: float) -> bool:
    """ This function compares the price that was purchased with the current price of the asset

    Args:
        percenteSell (float): Percentage of sale
        list_all_tickers (list): List with all assets
        symbolTicker (str): Tick ​​base
        priceCompare (float): price that was bought active

    Returns:
        bool: Boolean return signaling sale
    """
    result = list(filter(lambda tick : (tick['symbol'] == symbolTicker), list_all_tickers))
    price_compare_buy = float(format_Price_decimal_percente(priceCompare, percenteSell, 4))
    if price_compare_buy < float(result[0]['price']):
        return True
    return False


def get_price_current(list_all_tickers: list, symbolTicker: str) -> float:
    """This function returns the current price of an asset

    Args:
        list_all_tickers (list): List with all assets
        symbolTicker (str): Tick ​​base

    Returns:
        float: returns the current price
    """
    
    result = list(filter(lambda tick : (tick['symbol'] == symbolTicker), list_all_tickers))
    return round(float(result[0]['price']), 4)
    


def Dinamic_Buy(symbolTicker: str, symbolBase: str, client: object, percentePriceBUY: float, percentePriceStopBUY: float ) -> float:
    """This function returns a purchase value. Buying is dynamic, always trying to get the lowest price.

    Args:
        symbolTicker (str): cryptocurrency par symbol
        symbolBase (str): symbol of a single asset. EX: XRP
        client (object): Binance instance client
        percentePriceBUY (float): Percentage to purchase
        percentePriceStopBUY (float): Percentage to stop buying limit

    Returns:
        float: Returns the purchased amount
    """

    try:
        list_of_tickers = client.get_all_tickers()
        prev_symbolPrice = get_price_current(list_of_tickers, symbolTicker)
        quantityBuy = calculate_price_buy(symbolTicker, client)
        priceBuy = format_Price_decimal_percente(prev_symbolPrice, percentePriceBUY, 4)
        stopPriceBuy = format_Price_decimal_percente(prev_symbolPrice, percentePriceStopBUY, 4)
        quantityBuy = calculate_price_buy(symbolTicker, client)
        quantitySell = quantityBuy

        # buy order
        buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)
        status_list = client.get_all_orders(symbol=symbolTicker, orderId=buyOrder['orderId'])
        status = ''
        for get_status in status_list:
            if get_status['status'] == 'NEW':
                status = get_status['status']
                break

    except BinanceAPIException as e:
        print (e.status_code)
        print (e.message)
    

    while status == "NEW":
        checke_symbol_price = check_balance(symbolBase, client)
        
        print('status while ' , status)

        print(f"Balance in account {checke_symbol_price['price']}")
        time.sleep(5)

        list_of_tickers = client.get_all_tickers()
        current_symbolPrice = get_price_current(list_of_tickers, symbolTicker)

        print("    Prev Price = " + str(prev_symbolPrice))
        print(" Current Price = " + str(current_symbolPrice))

        if ( prev_symbolPrice > current_symbolPrice):

            result = client.cancel_order(
                symbol = symbolTicker,
                orderId = buyOrder.get('orderId')
            )

            quantityBuy = calculate_price_buy(symbolTicker, client)
            priceBuy = format_Price_decimal_percente(current_symbolPrice, percentePriceBUY, 4)
            stopPriceBuy = format_Price_decimal_percente(current_symbolPrice, percentePriceStopBUY, 4)
            quantityBuy = calculate_price_buy(symbolTicker, client)
            quantitySell = quantityBuy

            # buy order
            buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)
            status_list = client.get_all_orders(symbol=symbolTicker, orderId=buyOrder['orderId'])
            status = ''
            for get_status in status_list:
                if get_status['status'] == 'NEW':
                    status = get_status['status']
                    break
            prev_symbolPrice = current_symbolPrice
            if status == "NEW":
                continue

    print(f"{symbolTicker} purchased value {prev_symbolPrice}")
    return prev_symbolPrice
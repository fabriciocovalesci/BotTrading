from binance.client import Client, BinanceAPIException
from binance.enums import *
import numpy as np
import math
import time as t
from datetime import datetime, timezone

decimal_places = 6
amount_buy_usdt_to_btc = 120.00

def calculate_ma50(symbolTicker, client):
    ma50_local = 0
    sum = 0

    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "15 hour ago UTC")

    if (len(klines) == 60):

        for i in range(10,60):
            sum = sum + float(klines[i][4])

        ma50_local = sum / 50

    return ma50_local


def orderStatus(orderToCkeck, symbolTicker):
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

    t.sleep(1)

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
    get_quantity = float(balance['free'])
    if get_quantity == 0.0:
        return {"status": False, "quantity": get_quantity}
    return {"status": True, "quantity": get_quantity}



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
    print(" ActualMA50: "  + str(round(ma50,decimal_places)))
    print("ActualPrice: " + str(round(symbolPrice,decimal_places)))
    print(" PriceToBuy: "  + str(round(ma50*0.99,decimal_places)))
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
    price_compare_buy = float(format_Price_decimal_percente(priceCompare, percenteSell, decimal_places))
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
    return round(float(result[0]['price']), decimal_places)


def getId_data_base(list_table: list) -> int:
    """This function returns 'id' from the table

    Args:
        list_table (list): list with database query result

    Returns:
        int: Returns a valid table 'id'
    """
    id = None
    if len(list_table) > 0:
        for get_id in list_table:
            id = get_id[0]
        return id
    return id


def get_priceBuy_Quantity(list_table_report: list) -> dict:
    """This function returns a dict with the purchase price and the quantity purchased

    Args:
        list_table_report (list): List with the last buy record
        Ex: [(2, Decimal('1.5821'), 0, Decimal('0.0000'), 10, 'XRPUSDT', datetime.date(2021, 5, 2), False)]

    Returns:
        dict: Returns a dict with "price_buy" and "quantity"
    """
    
    dict_info = {
        "price_buy": None,
        "quantity" : None
    }
    if len(list_table_report) != 0:
        for get_info in list_table_report:
            dict_info['price_buy'] = get_info[1]
            dict_info['quantity'] = get_info[4]
        return dict_info
    return dict_info


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return int(math.floor(n * multiplier) / multiplier)

def calculate_profit(priceBuy: float, priceSell: float) -> float:
    return round(float((priceBuy/priceSell)*100),2)


def show_await(symbol: str, priceBuy: float, current_price: float, quantity: int, percenteSell: float) -> str:

    print(f"""
    ---------- {symbol} ---------------------
    | price buy:........... {priceBuy}
    | price sell:...........{float(format_Price_decimal_percente(priceBuy, percenteSell, decimal_places))}      
    | current price:....... {current_price} 
    | quantity for sale:... {quantity}      
    ---------------------------------------- 
    """)


def STARTING_SALE(symbolTicker: str, symbolBase: str, client: object, percentagePriceSELL: float, percentageStopPriceSELL: float, percentagestopLimitPriceSELL: float, dict_info: dict) -> dict:
    """[summary]

    Args:
        symbolTicker (str): [description]
        symbolBase (str): [description]
        client (object): [description]
        percentagePriceSELL (float): [description]
        percentageStopPriceSELL (float): [description]
        percentagestopLimitPriceSELL (float): [description]
        dict_info (dict): [description]

    Returns:
        dict: [description]
    """

    try:

        return_sell = {
            "priceSell": None,
            "quantity": None
        }
        list_of_tickers = client.get_all_tickers()
        symbolPriceSale = get_price_current(list_of_tickers, symbolTicker)

        priceSell = format_Price_decimal_percente(str(symbolPriceSale), percentagePriceSELL, decimal_places)
        stopPriceSell = format_Price_decimal_percente(str(symbolPriceSale), percentageStopPriceSELL, decimal_places)
        stopLimitPriceSell = format_Price_decimal_percente(str(symbolPriceSale), percentagestopLimitPriceSELL, decimal_places)

        if dict_info['price_buy'] == None and dict_info['quantity'] == None:
            print(f'Error in {dict_info}')

        quantitySell = round_down(dict_info['quantity'])

        orderOCO = sell_order_OCO(client, symbolTicker, quantitySell, priceSell, stopPriceSell, stopLimitPriceSell)

        while True:

            t.sleep(2)
            orders = client.get_open_orders(symbol=symbolTicker)
            if(len(orders) != 0):
                for key, value in orders[0].items():
                    if key == 'price':
                        return_sell['priceSell'] = value
                    if key == 'origQty':
                        return_sell["quantity"] = value
                print('Open Orders on Sale')
                t.sleep(5)
                continue
            else:
                return return_sell
                break

    except BinanceAPIException as e:
        print(e)
        with open("Error_Bot.txt", "a") as myfile:
            myfile.write(str(datetime.now().strftime("%d-%m-%y %H:%M:%S")) +" - an exception occured - {}".format(e)+ " Oops 3 ! \n")
        


def body_email_buy(symbolTicker: str, price_current: float, price_buy: float,percentagePriceSELL: float, quantity_buy: float) -> str:
    price = round(float(price_buy*quantity_buy), 3)
    price_sell = float(price_buy*percentagePriceSELL)
    html = f"""\
            <html>
            <head></head>
            <body>
                <h2><strong>Compra efetuada com sucesso &#129302; !!</strong></h2><br>
                <h3>Date: {str(datetime.now().strftime("%d-%m-%y %H:%M:%S"))} &#8986;</h3>
                <table style="width:70%">
                    <tr>
                        <th>Asset</th>
                        <th>Price Current</th>
                        <th>Price for Sale</th>
                        <th>Price Buy</th>
                        <th>Quantity</th>
                    </tr>
                    <tr>
                        <td style="text-align: center;">{symbolTicker}</td>
                        <td style="text-align: center;">{price_current} USDT</td>
                        <td style="text-align: center;">{price_sell} USDT</td>
                        <td style="text-align: center;">{price} USDT</td>
                        <td style="text-align: center;">{quantity_buy}</td>
                    </tr>
                </table>
            </body>
            </html>
            """
    return html

def body_email_sell(symbolTicker: str, price_current: float, price_buy: float,price_sell: float, profit: float, quantity_sell: float) -> str:
    price_sale = round(float(price_sell*quantity_sell), 3)
    html = f"""\
            <html>
            <head></head>
            <body>
                <h2><strong>Venda efetuada com sucesso &#129302; !!</strong></h2><br>
                <h3>Date: {str(datetime.now().strftime("%d-%m-%y %H:%M:%S"))} &#8986;</h3>
                <table style="width:70%">
                    <tr>
                        <th>Asset</th>
                        <th>Price Current</th>
                        <th>Price Sale</th>
                        <th>Price Buy</th>
                        <th>Quantity</th>
                        <th>Profit</th>
                    </tr>
                    <tr>
                        <td style="text-align: center;">{symbolTicker}</td>
                        <td style="text-align: center;">{price_current} USDT</td>
                        <td style="text-align: center;">{price_sale} USDT</td>
                        <td style="text-align: center;">{price_buy} USDT</td>
                        <td style="text-align: center;">{quantity_sell}</td>
                        <td style="text-align: center;">{profit} USDT</td>
                    </tr>
                </table>
            </body>
            </html>
            """
    return html


def SELL_MARKET(symbolTicker: str, quantity: int, client: object) -> dict:
    """ This function executes a market sales order

    Args:
        symbolTicker (str): Pair symbol crypto
        quantity (int): Quantity for sale
        client (object): Binance API Client Instance

    Returns:
        dict: Returns a dict with sale information
    """
    
    try:
        order = client.order_market_sell(symbol=symbolTicker,quantity=quantity)
        return order
    except BinanceAPIException as error:
        print(f"Error on sell market {error}")


def quantity_bitcoin(crypto, client, amount_buy_usdt):
    """This function returns the amount of satoshi to buy

    Args:
        crypto (str): BTCUSDT pair
        client (object): platform authenticated client
        amount_buy_usdt (floar): Value in USDT

    Returns:
        [float]: Returns the amount of bitcoin for purchase
    """
    try:
        current_price = client.get_symbol_ticker(symbol=crypto)
        get_price = float(current_price['price'])
        satoshi = amount_buy_usdt / get_price * 100000000
        quantity_btc = round(float(satoshi / 100000000), 6)
        return quantity_btc
    except BinanceAPIException as error:
        print(f"Error calculate quantity of bitcoin {error}")



def Dinamic_Buy_Bitcoin(symbolTicker: str, symbolBase: str, client: object, percentePriceBUY: float, percentePriceStopBUY: float ) -> float:
    """This function returns a purchase value. Buying is dynamic, always trying to get the lowest price.

    Args:
        symbolTicker (str): cryptocurrency par symbol
        symbolBase (str): symbol of a single asset. EX: BTC
        client (object): Binance instance client
        percentePriceBUY (float): Percentage to purchase
        percentePriceStopBUY (float): Percentage to stop buying limit

    Returns:
        float: Returns the purchased amount
    """

    return_buy = {
        "amount_buy": 0.0,
        "quantity": 0,
        "order_id": 0
    }
    status = 'NEW'

    try:
        list_of_tickers = client.get_all_tickers()
        prev_symbolPrice = get_price_current(list_of_tickers, symbolTicker)
        quantityBuy = quantity_bitcoin(symbolTicker, client, amount_buy_usdt_to_btc)
        priceBuy = format_Price_decimal_percente(prev_symbolPrice, percentePriceBUY, decimal_places)
        stopPriceBuy = format_Price_decimal_percente(prev_symbolPrice, percentePriceStopBUY, decimal_places)

        quantityBuy = quantity_bitcoin(symbolTicker, client, amount_buy_usdt_to_btc)

        t.sleep(3)
        # buy order
        buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)

        return_buy['amount_buy'] = priceBuy
        return_buy['order_id'] = buyOrder['orderId']

        status_list = client.get_all_orders(symbol=symbolTicker, orderId=buyOrder['orderId'])
        for get_status in status_list:
            if get_status['status'] == 'NEW':
                status = get_status['status']
                break

    except BinanceAPIException as e:
        print (e.status_code)
        print (e.message)
    

    while status == 'NEW':

        checke_symbol_price = check_balance(symbolBase, client)
        
        print('status while ' , status)


        print(f"Balance in account {checke_symbol_price['quantity']}")
        t.sleep(3)

        list_of_tickers = client.get_all_tickers()
        current_symbolPrice = get_price_current(list_of_tickers, symbolTicker)
        price_current_BTCUSDT = (current_symbolPrice*float(checke_symbol_price['quantity']))


        if price_current_BTCUSDT > 12.00:
            print(f"Balance in account {checke_symbol_price['quantity']}")
            return_buy['quantity'] = checke_symbol_price['quantity']
            break

        print("    Prev Price = " + str(prev_symbolPrice))
        print(" Current Price = " + str(current_symbolPrice))

        if ( prev_symbolPrice > current_symbolPrice):

            try:

                result = client.cancel_order(
                    symbol = symbolTicker,
                    orderId = buyOrder['orderId']
                )

                priceBuy = format_Price_decimal_percente(current_symbolPrice, percentePriceBUY, decimal_places)
                stopPriceBuy = format_Price_decimal_percente(current_symbolPrice, percentePriceStopBUY, decimal_places)
                quantityBuy = quantity_bitcoin(symbolTicker, client, amount_buy_usdt_to_btc)

                # buy order
                buyOrder = buy_stop_loss_limit(client, symbolTicker, quantityBuy, priceBuy ,stopPriceBuy)
                return_buy['amount_buy'] = priceBuy
                return_buy['order_id'] = buyOrder['orderId']

                status_list = client.get_all_orders(symbol=symbolTicker, orderId=buyOrder['orderId'])
                for get_status in status_list:
                    if get_status['status'] == 'NEW':
                        status = get_status['status']
                        break

                prev_symbolPrice = current_symbolPrice
                print('-- ', status)
                if status == "NEW":
                    continue
            except BinanceAPIException as e:
                print(f'An exception occurred {e}')
                print(f"status {e.status_code}")
                print(f'Message {e.message}')
                continue

    print(f"{symbolTicker} purchased value {prev_symbolPrice}")
    return return_buy
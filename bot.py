from binance.client import Client
from binance.enums import *
from tradingview_ta import TA_Handler, Interval, Exchange
import datetime
import random
import time
from datetime import datetime
import config
from sendEmail import SendEmail, SendEmailDeploy

client = Client(config.API_KEY, config.API_SECRET, tld='com')


while 1:

    SendEmailDeploy()
    now = datetime.now()
    fecha = now.strftime("%d-%m-%y %H:%M:%S")
    lista = client.get_all_tickers()
    strongBuy_list = []
    strongSell_list = []
    for i in lista:
        tesla = TA_Handler()
        tesla.set_symbol_as(i['symbol'])
        tesla.set_exchange_as_crypto_or_stock("BINANCE")
        tesla.set_screener_as_crypto()
        tesla.set_interval_as(Interval.INTERVAL_1_HOUR)
        print(i['symbol'])
        try:
            print(tesla.get_analysis().summary)
        except Exception as e:
            print("No Data")
        continue
        if((tesla.get_analysis().summary)["RECOMMENDATION"])=="STRONG_BUY":
            print(f" COMPRA FORTE {i}", fecha)
            strongBuy_list.append(i['symbol'])
        elif((tesla.get_analysis().summary)["RECOMMENDATION"])=="STRONG_SELL":
            print(f" VENDA FORTE {i}", fecha)
            strongSell_list.append(i['symbol'])
    
    Buy = strongBuy_list
    Sell = strongSell_list
    
    print(F'Recomendacao de Compra {Buy}')

    print(F'Recomendacao de Venda {Sell}')
    
    SendEmail(Buy, Sell)

    time.sleep(300)
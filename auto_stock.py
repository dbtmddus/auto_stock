from pickle import FALSE, TRUE
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler 
from stocklab.agent.ebest import EBest
from stocklab.db_handler.mongodb_handler import MongoDBHandler
from multiprocessing import Process
import schedule

ebest_demo = EBest("DEMO")
ebest_demo.login()
mongo = MongoDBHandler()

  
def trading_scenario(code):
    result = ebest_demo.get_current_call_price_by_code(code)
    trading_scenario.price = int(result[0]["현재가"])

    if (trading_scenario.firstCall == False):
        change = trading_scenario.price/trading_scenario.prePrice;
        print("가격변동" , trading_scenario.prePrice, "->", trading_scenario.price, "change:", change)

        if ( change > 1.001 ):
            order = ebest_demo.order_stock(code, "2", str(trading_scenario.price), "2", "03") 
            print("매수")
        elif ( change < 0.999 ):
            order = ebest_demo.order_stock(code, "2", str(trading_scenario.price), "1", "03")         
            print("매도")
    trading_scenario.prePrice = trading_scenario.price
    trading_scenario.firstCall = False
trading_scenario.prePrice = 0
trading_scenario.firstCall = True


if __name__ == '__main__':
    code = "005930"
    schedule.every(3).seconds.do(trading_scenario, code)
    while True:
        schedule.run_pending()
        print("waiting...")
        time.sleep(1)
 
#    print(ebest_demo.get_current_call_price_by_code("005930"))
    #order = ebest_demo.order_stock("005930", "1", "0", "2", "03")
#    print( ebest_demo.get_current_call_price_by_code("035720") )
 #   print( ebest_demo.get_jango() )

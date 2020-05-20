from tqsdk import TqApi, TargetPosTask, TqSim, InsertOrderTask, TqAccount, TqReplay, TqBacktest, BacktestFinished
from contextlib import closing
from datetime import date, datetime
from pandas import Series, DataFrame
import pandas as pd


acc = TqSim()
symbol = "SHFE.ni2008"
一跳价格 = 10.0
volume = 1  # 每次下单数
status = '等待开仓'
check_tick = 10

def 开始交易():



try:
    api = TqApi(acc, backtest=TqBacktest(start_dt=datetime(2020, 5, 11,21,1,2,795738,) ,end_dt=datetime(2020, 5, 11,22,1,0,0)),web_gui=True)
    # api = TqApi(acc, web_gui=True)
    ticks = api.get_tick_serial(symbol)
    klines = api.get_kline_serial(symbol,60)
    行情 = api.get_quote(symbol)
    上一个价格 = 行情.bid_price1

    while True:
        api.wait_update()
        print(status)
        # 检测挂价订单(行情,ticks)
        # 持仓检测模块(行情,ticks)
        start_trade(行情, ticks)
        委托挂单(行情, ticks)
        检测挂价订单(行情, ticks)
        平仓检测(行情, ticks)
        print(api.get_account().balance)




except BacktestFinished as e:
    print(acc.trade_log)

    pass
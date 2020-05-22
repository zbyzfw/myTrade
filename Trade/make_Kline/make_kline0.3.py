from tqsdk import TqApi, TargetPosTask, TqSim, InsertOrderTask, TqAccount, TqReplay, TqBacktest, BacktestFinished
from contextlib import closing
from datetime import date, datetime
from pandas import Series, DataFrame
import pandas as pd

'''
此策略根据k线趋势:
k线大于上一根k线最高值,每次tick上涨一直做多,如果持有有空仓,全平,然后做多.
k线小于上一根k线最小值,每次tick下跌一直做空,如果有持有多仓,全平,然后做空.
'''

acc = TqSim()
symbol = "SHFE.ni2008"
# symbol = 'DCE.pp2009'

一跳价格 = 10.0
volume = 1  # 每次下单数
status = '等待开仓'
check_tick = 10
挂多单子列表 = {}
# 多单价格列表 = []
挂空单子列表 = {}
target_volume = 1  # 目标持仓手数
空持仓 = 0
多持仓 =0


def 开始交易(行情,klines):
    global 上一根k线的最高价,上一根k线的最低价,上一个价格,status,target_volume,空持仓,多持仓
    data = api.get_position(symbol)
    多仓之和 = data['pos_long_today']
    空仓之和 = data['pos_short_today']
    if status == '等待开仓':
        #     #     return

        上一根k线的最高价 = klines.iloc[-2].high
        上一根k线的最低价 = klines.iloc[-2].low
        print(上一根k线的最低价, 上一根k线的最高价, 上一个价格, 行情.bid_price1)
        # oldt = 上一个价格
        newt = 行情.ask_price1
        # print(oldt, '1', newt, 行情.datetime)
        if newt > 上一根k线的最高价:
            print('涨破上一个价格的最高价')
            status = '做多'
            # target_volume=0
            # target_pos.set_target_volume(target_volume)
            # 做多(行情)
            # 上一个价格 = newt
        elif newt < 上一根k线的最低价:
            print('跌破上一个价格的最低价')
            status = '做空'
            # target_volume = 0
            # target_pos.set_target_volume(target_volume)
            # 做空(行情)
        #     上一个价格 = newt
        # else:
        #     上一个价格 = newt
            # status = '等待开仓'
    elif status == '做多':
        #     #     return
        上一根k线的最高价 = klines.iloc[-2].high
        上一根k线的最低价 = klines.iloc[-2].low
        print(上一根k线的最低价,上一根k线的最高价,行情.ask_price1,行情.bid_price1)
        # oldt = 上一个价格
        newt = 行情.ask_price1
        # print(oldt, '1', newt, 行情.datetime)
        if newt > 上一根k线的最高价:
            print('涨破上一个价格的最高价')
            status = '做多'
            # target_volume=0
            # target_pos.set_target_volume(target_volume)
            # 做多(行情)
            # 上一个价格 = newt
        elif newt < 上一根k线的最低价:
            print('跌破上一个价格的最低价')
            status = '做空'
            target_volume = 多持仓
            对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='CLOSETODAY', volume=多持仓)
            多持仓 = 0

            # target_pos.set_target_volume(target_volume)
            # 做空(行情)
        #     上一个价格 = newt
        # else:
        #     上一个价格 = newt
            # status = '等待开仓'
    elif status == '做空':
        上一根k线的最高价 = klines.iloc[-2].high
        上一根k线的最低价 = klines.iloc[-2].low
        print(上一根k线的最低价, 上一根k线的最高价, 行情.ask_price1, 行情.bid_price1)
        # oldt = 上一个价格
        newt = 行情.ask_price1
        # print(oldt, '1', newt, 行情.datetime)
        if newt > 上一根k线的最高价:
            print('涨破上一个价格的最高价')
            status = '做多'
            target_volume= 空持仓
            # target_pos.set_target_volume(target_volume)
            对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSETODAY', volume=空持仓)
            空持仓 = 0
            # 上一个价格 = newt
        elif newt < 上一根k线的最低价:
            print('跌破上一个价格的最低价')
            status = '做空'
            # target_volume = 0
            # target_pos.set_target_volume(target_volume)
            # 做空(行情)
        #     上一个价格 = newt
        # else:
        #     上一个价格 = newt
            # status = '等待开仓'

def 开仓(行情,ticks):
    global status,target_volume,上一个价格,总持仓,对价订单,空持仓,多持仓
    data = api.get_position(symbol)
    oldt = 上一个价格
    newt = 行情.bid_price1
    # print(ticks)
    print(oldt, '1', newt, 行情.datetime)
    多仓之和 = data['pos_long_his'] + data['pos_long_today']
    空仓之和 = data['pos_short_his'] + data['pos_short_today']
    if status == '做多':
        if (oldt < newt):
            target_volume = 1
            对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=target_volume)
            多持仓 += 1
            上一个价格 = newt
            # target_pos.set_target_volume(target_volume)
    elif status == '做空':
        if (oldt > newt):
            target_volume = 1
            对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=target_volume)
            空持仓 +=1
            上一个价格 = newt
    else:
        上一个价格 = newt
            # target_pos.set_target_volume(target_volume)

def 检测挂价订单(行情):
    global 挂价订单, status
    if status == "检测挂价订单委托":
        a = api.get_order(对价订单['order_id'])
        # 委托价格1 = a['limit_price']
        未成交手数1 = a['volume_left']
        # 挂单方向1 = a["direction"]
        # 未成交手数
        是否确定已报入交易所 = a.is_online
        if 是否确定已报入交易所:
            status = '等待开仓'
            return
        if 未成交手数1 == 0:
            status = '等待开仓'
            return
        if a.status == 'ALIVE':
            status = '等待开仓'
            return

        if a.status == 'FINISHED':
            status = '等待开仓'
            return
        else:
            status = "检测挂价订单委托"
            return

            # if ticks.iloc[-1].ask_price not in 挂多单子列表.values():
            #     if 空仓之和 <= 多仓之和:  # 做多时多仓多,只做一手
            #         print('做多时多>=空')
            #         status = '等待开仓成交'
            #         # 对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=1)
            #         target_volume+=volume
            #         对价订单 =target_pos.set_target_volume(target_volume)#目标持仓手数，正数表示多头，负数表示空头，0表示空仓
            #         # 挂多单子列表.append(对价订单.order_id)
            #         # 挂多单子列表[对价订单.order_id]=行情.ask_price1
            #         开单数量 = 1
            #         # 上一个价格 = newt
            #     elif 多仓之和 < 空仓之和:  # 做多时空仓多,补齐多仓
            #         print('做多时空大于多')
            #         status = '等待开仓成交'
            #         订单数量差 = 空仓之和 - 多仓之和
            #         对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=订单数量差)
            #         # 挂多单子列表.append(对价订单.order_id)
            #         # 挂多单子列表[对价订单.order_id]=行情.ask_price1
            #         开单数量 = 订单数量差
            #         # 上一个价格 = newt

try:
    api = TqApi(acc, backtest=TqBacktest(start_dt=datetime(2020, 5, 12,21,1,2,795738,) ,end_dt=datetime(2020, 5, 13,14,59,59,0)),web_gui=True)
    # api = TqApi(acc, web_gui=True)
    ticks = api.get_tick_serial(symbol,5)
    klines = api.get_kline_serial(symbol,10,5)
    行情 = api.get_quote(symbol)
    上一个价格 = 行情.bid_price1
    target_pos = TargetPosTask(api, symbol)

    while True:
        api.wait_update()
        print(status)
        开始交易(行情,klines)
        开仓(行情,ticks)





except BacktestFinished as e:
    print(acc.trade_log)

    pass
from tqsdk import TqApi, TargetPosTask, TqSim, InsertOrderTask, TqAccount, TqReplay, TqBacktest, BacktestFinished
from contextlib import closing
from datetime import date, datetime
from pandas import Series, DataFrame
import pandas as pd


acc = TqSim()
# symbol = "SHFE.ni2008"
symbol = 'DCE.pp2009'

一跳价格 = 1.0
volume = 1  # 每次下单数
status = '等待开仓'
check_tick = 10
挂多单子列表 = {}
# 多单价格列表 = []
挂空单子列表 = {}

def 开始交易(行情,klines):
    global 上一根k线的最高价,上一根k线的最低价,上一个价格,status
    if status == '等待开仓':
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
            # 做多(行情)
            上一个价格 = newt
        elif newt < 上一根k线的最低价:
            print('跌破上一个价格的最低价')
            status = '做空'
            # 做空(行情)
            上一个价格 = newt
        else:
            上一个价格 = newt
            status = '等待开仓'

def 做空(行情):
    global status,上一个价格,挂空单子列表,挂多单子列表,对价订单,开单数量
    if status == '做空':
        oldt = 上一个价格
        newt = 行情.ask_price1
        print(oldt, '1', newt, 行情.datetime)
        data = api.get_position(symbol)
        多仓之和 = data['pos_long_his'] + data['pos_long_today']
        空仓之和 = data['pos_short_his'] + data['pos_short_today']
        # 开空单价格=newt-一跳价格
        # 开多单价格=行情.ask_price1+一跳价格
        print(newt not in 挂空单子列表.values())
        print(newt in 挂空单子列表.values())
        print(行情.ask_price1 in 挂多单子列表.values())
        if (oldt > newt):  # and (开空单价格 not in 挂空单子列表.values()):#价格下跌,做空
            if 行情.bid_price1 not in 挂空单子列表.values():
                if 多仓之和 <= 空仓之和:  # 开仓的情况
                    print('多<=空')
                    对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=1)
                    # 挂空单子列表[对价订单.order_id] = 行情.bid_price1
                    开单数量 = 1
                    上一个价格 = newt
                    status = '等待开仓成交'
                elif 多仓之和 > 空仓之和:
                    print('多大于空')
                    订单数量差 = 多仓之和 - 空仓之和
                    对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=订单数量差)
                    # 挂空单子列表[对价订单.order_id]=行情.bid_price1
                    开单数量 = 订单数量差
                    上一个价格 = newt
                    status = '等待开仓成交'
                # else:
                #     print('请检查多单持仓')
                #     status = '等待开仓'
                #     上一个价格 = newt

            elif 行情.bid_price1 in 挂空单子列表.values():  # 此价格已开单，不更新oldt
                status = '等待开仓'
                # 上一个价格 = newt#实际账号操作时，此处需要修改
                print('运行持仓检测模块')
        else:
            上一个价格 = newt

def 做多(行情):
    global status, 上一个价格, 挂空单子列表, 挂多单子列表,开单数量,对价订单
    if status == '做多':
        oldt = 上一个价格
        newt = 行情.ask_price1
        print(oldt, '1', newt, 行情.datetime)
        data = api.get_position(symbol)
        多仓之和 = data['pos_long_his'] + data['pos_long_today']
        空仓之和 = data['pos_short_his'] + data['pos_short_today']
        if (oldt < newt):
            if newt not in 挂多单子列表.values():  # 价格上涨,做多
                if 空仓之和 <= 多仓之和:  # 做多时多仓多,只做一手
                    print('做多时多=空')
                    status = '等待开仓成交'
                    对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=1)
                    # 挂多单子列表.append(对价订单.order_id)
                    # 挂多单子列表[对价订单.order_id]=行情.ask_price1
                    开单数量 = 1
                    上一个价格 = newt
                elif 多仓之和 < 空仓之和:  # 做多时空仓多,补齐多仓
                    print('做多时空大于多')
                    status = '等待开仓成交'
                    订单数量差 = 空仓之和 - 多仓之和
                    对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=订单数量差)
                    # 挂多单子列表.append(对价订单.order_id)
                    # 挂多单子列表[对价订单.order_id]=行情.ask_price1
                    开单数量 = 订单数量差
                    上一个价格 = newt
                # else:
                #     多仓之和 > 空仓之和
                #     status = '等待开仓'
                #     上一个价格 = newt
            else:  # 等待此价格平仓
                status = '等待开仓'
                # 上一个价格 = newt
                print('运行持仓检测模块，等待此价格平仓')
        else:
            上一个价格 = newt

def 委托挂单(行情, klines):
    global 挂价订单, status, 对价订单
    if status == "等待开仓成交":
        a = api.get_order(对价订单.order_id)
        data = api.get_position(symbol)
        多仓之和 = data['pos_long_his'] + data['pos_long_today']
        空仓之和 = data['pos_short_his'] + data['pos_short_today']
        未成交手数1 = a['volume_left']  # 单指此订单的未成交数量
        开单方向1 = a["direction"]

        print(多仓之和, 空仓之和)

        if a.is_error:
            status = "等待开仓"  # 进入下一个循环
            print('错单')
            return
        if a['volume_left'] != 0:
            status = "等待开仓成交"  # 进入下一个循环
            print("未成交---", 未成交手数1)
            return
        if a.is_dead:
            print('开单成交---')
            if 开单方向1 == "BUY" and a.offset == 'OPEN':
                挂单数量 = 开单数量
                print(a.trade_price)
                挂价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='CLOSETODAY', volume=挂单数量,
                                        limit_price=行情.ask_price1 + 一跳价格)
                挂多单子列表[挂价订单.order_id] = 行情.ask_price1

                status = '检测挂价订单委托'
            elif 开单方向1 == 'SELL' and a.offset == 'OPEN':
                挂单数量 = 开单数量
                # 当前价格 = ticks["ask_price1"].tolist()[-1] - 一跳价格#SELL
                挂价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSETODAY', volume=挂单数量,
                                        limit_price=行情.bid_price1 - 一跳价格)
                挂空单子列表[挂价订单.order_id] = 行情.bid_price1
                status = '检测挂价订单委托'

def 检测挂价订单(行情):
    global 挂价订单, status
    if status == "检测挂价订单委托":
        a = api.get_order(挂价订单['order_id'])
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

def 平仓检测(行情,klines):
    global status,挂多单子列表,挂空单子列表
    if status=="等待开仓":
        持仓检测模块(行情,klines)
        # 固定止损止盈(行情,ticks)
        # 一分钟检测(行情,ticks)

def 持仓检测模块(行情, ticks):  # 第三步
    global 挂多单子列表,挂空单子列表,status
    data = api.get_position(symbol)
    order1 = api.get_order()
    # a = list(data.orders.values())
    for order_id in list(挂多单子列表.keys()):
        print(order1[order_id].status)
        if order1[order_id].status == 'FINISHED':
            del 挂多单子列表[order_id]
    print(挂多单子列表)
    for order_id in list(挂空单子列表.keys()):
        if order1[order_id].status == 'FINISHED':
            del 挂空单子列表[order_id]
    print(挂空单子列表)
    status = '等待开仓'


try:
    api = TqApi(acc, backtest=TqBacktest(start_dt=datetime(2020, 5, 12,21,1,2,795738,) ,end_dt=datetime(2020, 5, 13,14,59,59,0)),web_gui=True)
    # api = TqApi(acc, web_gui=True)
    ticks = api.get_tick_serial(symbol,2)
    klines = api.get_kline_serial(symbol,60,5)
    行情 = api.get_quote(symbol)
    上一个价格 = 行情.ask_price1

    while True:
        api.wait_update()
        print(status)
        开始交易(行情,klines)
        做多(行情)
        做空(行情)
        委托挂单(行情,klines)
        检测挂价订单(行情)
        平仓检测(行情,klines)





except BacktestFinished as e:
    print(acc.trade_log)

    pass
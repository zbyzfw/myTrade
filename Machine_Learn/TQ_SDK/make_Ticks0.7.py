from tqsdk import TqApi, TargetPosTask, TqSim, InsertOrderTask, TqAccount, TqReplay, TqBacktest, BacktestFinished
from contextlib import closing
from datetime import date, datetime
from pandas import Series, DataFrame
import pandas as pd

# api = TqApi(TqSim(),web_gui=True)
acc = TqSim()
symbol = "SHFE.rb2010"
一跳价格 = 1.0
volume = 1  # 每次下单数
status = '等待开仓'
check_tick = 10
# open_Trade =
平仓时间 = '下午14:59:30-55秒'
委托远离几跳撤单 = 10
委托间隔多少秒撤单 = 120
保本损改变条件 = 20
止损 = 10  # 十跳止损
止盈 = 30  # 30跳止盈
波动开仓跳数 = 10
止损临时 = 0
委托订单 = 0
委托时间 = 0
挂多单子列表 = {}
# 多单价格列表 = []
挂空单子列表 = {}
# 空单价格列表 = []


def 时间格式化(TIM):
    TIM = Series(TIM)
    TIM = TIM.apply(lambda x: int(x))
    TIM = pd.to_datetime(TIM, unit='ns').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    TIM = TIM.dt.strftime('%Y-%m-%d %H:%M:%S')
    return TIM


def start_trade(行情, ticks):  # 开仓判断
    global status, 止损临时, 委托时间, 对价订单, 上一个价格,开单数量
    # sd=ticks[-1].ask_price1
    # ticks['last_price'].tolist()[-2]
    # print(ticks[0:10])
    print('!__!__!')
    if status == '等待开仓':
        oldt = 上一个价格
        newt = 行情.bid_price1
        print(oldt, '1', newt, 行情.datetime)
        data = api.get_position(symbol)
        多仓之和 = data['pos_long_his'] + data['pos_long_today']
        空仓之和 = data['pos_short_his'] + data['pos_short_today']
        开空单价格=newt-一跳价格
        开多单价格=行情.ask_price1+一跳价格
        print(newt-一跳价格 in 挂空单子列表)
        print(行情.ask_price1 in 挂多单子列表)
        if (oldt > newt) and (开空单价格 not in 挂空单子列表.values()):#价格下跌,做空
            if 空仓之和 >= 多仓之和:#做空时空仓多,不存在这种情况
                status = '等待开仓'
                print('做空时空仓多,不应该存在这种情况')
                # 对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=1)
                #
                # 多单价格列表.append(对价订单.trade_price)
                开单数量 = 1
                上一个价格 = newt
            else:#做空时多仓多,补齐空仓
                status = '等待开仓成交'
                订单数量差 = 多仓之和 - 空仓之和
                对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=订单数量差)
                挂空单子列表[对价订单.order_id]=行情.bid_price1
                # 多单价格列表.append(对价订单.trade_price)
                开单数量 = 订单数量差
                上一个价格 = newt
        elif (oldt > newt) and (开空单价格 in 挂空单子列表.values()):#价格下跌,做空
            if 空仓之和 >= 多仓之和:#做空时空仓多,且已经有空仓记录,不再下单
                status = '等待开仓'
                print('做空时空仓多,不应该存在这种情况')
                上一个价格 = newt
            else:#做空时多仓多,补齐空仓
                status = '等待开仓成交'
                订单数量差 = 多仓之和 - 空仓之和
                对价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='OPEN', volume=订单数量差)

                # 多单价格列表.append(对价订单.trade_price)
                开单数量 = 订单数量差
                上一个价格 = newt

        elif (oldt < newt) and (开多单价格 not in 挂多单子列表.values()):#价格上涨,做多
            if 多仓之和 >= 空仓之和:#做多时多仓多,只做一手
                status = '等待开仓成交'
                对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=1)
                # 挂多单子列表.append(对价订单.order_id)
                # 挂多单子列表[对价订单.order_id]=行情.ask_price1
                开单数量=1
                上一个价格 = newt
            else:#做多时空仓多,补齐多仓
                status = '等待开仓成交'
                订单数量差 = 空仓之和 - 多仓之和
                对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=订单数量差)
                # 挂多单子列表.append(对价订单.order_id)
                # 挂多单子列表[对价订单.order_id]=行情.ask_price1
                开单数量 = 订单数量差
                上一个价格 = newt
        elif (oldt - newt < 0) and (开多单价格 in 挂空单子列表.values()):#价格上涨且已有空单记录,做多
            if 多仓之和 >= 空仓之和:  # 做多时多仓多,且已有记录,不在下单
                status = '等待开仓'
                上一个价格 = newt
            else:#做多时空仓多,补齐多仓
                status = '等待开仓成交'
                订单数量差 = 空仓之和 - 多仓之和
                对价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='OPEN', volume=订单数量差)
                # 挂多单子列表.append(对价订单.order_id)
                # 挂多单子列表[对价订单.order_id]=行情.ask_price1
                开单数量=订单数量差
                上一个价格 = newt
        else:
            status = '等待开仓'
            print("-------------")


def 委托挂单(行情, ticks):
    global 挂价订单, status, 对价订单
    if status == "等待开仓成交":
        a = api.get_order(对价订单.order_id)
        data = api.get_position(symbol)
        多仓之和 = data['pos_long_his'] + data['pos_long_today']
        空仓之和 = data['pos_short_his'] + data['pos_short_today']
        委托价格1 = a['limit_price']
        未成交手数1 = a['volume_left']  # 单指此订单的未成交数量
        开单方向1 = a["direction"]
        下单时间 = a['insert_date_time']

        # 是否报入交易所 = a.is_online
        print(多仓之和, 空仓之和)

        if a.is_error:
            status = "等待开仓"  # 进入下一个循环
            print('错单')
            return
        # if a.is_online != True:
        #     status = "等待开仓成交"#进入下一个循环
        #     print('未报入交易所---',a.is_online)
        #     return
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
                挂空单子列表[挂价订单.order_id] = 行情.ask_price1

                # if tick =
                status = '检测挂价订单委托'
            elif 开单方向1 == 'SELL' and a.offset == 'OPEN':
                挂单数量 = 开单数量
                    # 当前价格 = ticks["ask_price1"].tolist()[-1] - 一跳价格#SELL
                挂价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSETODAY', volume=挂单数量,
                                            limit_price=行情.bid_price1 - 一跳价格)
                挂多单子列表[挂价订单.order_id] = 行情.bid_price1
                status = '检测挂价订单委托'


def 检测挂价订单(行情, ticks):
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
        if a.status == 'ACTIVE':
            status = '等待开仓'
            return

        if a.status == 'FINISHED':
            status = '等待开仓'
            return
        else:
            status = "检测挂价订单委托"
            return
        # if 挂单方向1 == "BUY":
        #     当前价格 = ticks["bid_price1"].tolist()[-1]
        # else:
        #     当前价格 = ticks["ask_price1"].tolist()[-1]#SELL
        # 下单时间 = a['insert_date_time']
        # if 未成交手数1 != 0:
        #     当前状态 = "等待平仓"#执行平仓检测
        #     print("执行平仓检测")
        #     return
        # if abs(委托价格1 - 当前价格) > 委托远离几跳撤单 * 一跳价格:
        #     api.cancel_order(委托订单['order_id'])#取消远离成交的订单
        #     status = '寻找开仓机会'
        #     print("远离挂单,撤单了")
        #     print("委托价格", 委托价格1)
        #     print("当前价格", 当前价格)
        #     return
        # if (ticks["datetime"].tolist()[-1] - 委托时间) / 1000000000 > 委托间隔多少秒撤单:
        #     api.cancel_order(委托订单['order_id'])#取消挂单时间过长的单子
        #     status = '寻找开仓机会'
        #     print("挂单太久,撤单了")
        #     return


def 持仓检测模块(行情, ticks):  # 第三步
    global symbol
    data = api.get_position(symbol)
    order1 = api.get_order()
    tader = api.get_trade()
    # print(data)
    多仓之和 = data['pos_long_his'] + data['pos_long_today']
    多仓成本 = data['open_price_long']
    空仓之和 = data['pos_short_his'] + data['pos_short_today']
    空仓成本 = data['open_price_short']
    当前价格 = ticks["last_price"].tolist()[-1]
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
    #
    # if 多仓之和 != 0:
    #     status = '等待平仓'
    #     print('暂不挂单')

    # if 多仓之和>0:
    #     if 当前价格>多仓成本+保本损改变条件*一跳价格:
    #         止损临时=0
    # else:
    #     if 空仓成本>当前价格+保本损改变条件*一跳价格:
    #         止损临时=0


def 固定止损止盈(行情, ticks):
    global status
    data = api.get_position(symbol)
    多仓之和 = data['pos_long_his'] + data['pos_long_today']
    多仓成本 = data['open_price_long']
    空仓之和 = data['pos_short_his'] + data['pos_short_today']
    空仓成本 = data['open_price_short']
    当前价格 = ticks["last_price"].tolist()[-1]
    当前时间 = ticks['datetime'].tolist()[-1]

    if 当前时间 > 平仓时间:
        平所有(symbol)
        status = '终止交易'
    # if 多仓之和>0:
    #     if 当前价格>=多仓成本+止盈*一跳价格:
    #         平所有(symbol)
    #         print("止盈")
    #         当前状态="寻找开仓机会"
    #     if 当前价格<=多仓成本-止损临时*一跳价格:
    #         平所有(symbol)
    #         print(止损)
    #         当前状态="寻找开仓机会"
    # else:
    #     if 当前价格<=空仓成本-止盈*一跳价格:
    #         平所有(symbol)
    #         print(止盈)
    #         当前状态="寻找开仓机会"
    #     if 当前价格>=空仓成本+止损临时*一跳价格:
    #         平所有(symbol)#调用平所有函数
    #         print(止损)
    #         当前状态="寻找开仓机会"


def 平所有(symbol):  # 直接用
    data = api.get_position(symbol)
    多仓1 = data['pos_long_his']
    多仓2 = data['pos_long_today']
    空仓1 = data['pos_short_his']
    空仓2 = data['pos_short_today']

    if 多仓1 != 0:
        api.insert_order(symbol=symbol, direction="SELL", offset="CLOSE", volume=多仓1)
    if 多仓2 != 0:
        if symbol[:4] == "SHFE":
            api.insert_order(symbol=symbol, direction="SELL", offset="CLOSETODAY", volume=多仓2)
        else:
            api.insert_order(symbol=symbol, direction="SELL", offset="CLOSE", volume=多仓2)
    if 空仓1 != 0:
        api.insert_order(symbol=symbol, direction="BUY", offset="CLOSE", volume=空仓1)
    if 空仓2 != 0:
        if symbol[:4] == "SHFE":
            api.insert_order(symbol=symbol, direction="BUY", offset="CLOSETODAY", volume=空仓2)
        else:
            api.insert_order(symbol=symbol, direction="BUY", offset="CLOSE", volume=空仓2)


# def 一分钟检测(行情,ticks):
#     global status
#     mymax=行情['high'].tolist()[-1]
#     mymin=行情['low'].tolist()[-1]
#     if mymax-mymin>单根1分钟超过多少平仓*一跳价格:
#         平所有(symbol)
#         print("波动太大平仓")
#         status="寻找开仓机会"


def 平仓检测(行情,ticks):
    global status
    if status=="等待开仓":
        持仓检测模块(行情,ticks)
        # 固定止损止盈(行情,ticks)
        # 一分钟检测(行情,ticks)

try:
    # api = TqApi(acc, backtest=TqBacktest(start_dt=datetime(2020, 5, 11,21,1,2,795738,) ,end_dt=date(2020, 5, 15)),web_gui=True)
    api = TqApi(acc, web_gui=True)
    ticks = api.get_tick_serial(symbol)
    行情 = api.get_quote(symbol)
    上一个价格 = 行情.bid_price1
    while True:
        api.wait_update()
        print(status)
        # 检测挂价订单(行情,ticks)
        start_trade(行情, ticks)
        委托挂单(行情, ticks)
        检测挂价订单(行情, ticks)
        平仓检测(行情, ticks)



except BacktestFinished as e:
    print(acc.trade_log)
    pass

api.close()

#%%
from tqsdk import TqApi,TargetPosTask,TqSim,InsertOrderTask,TqAccount,TqReplay,TqBacktest,BacktestFinished
from contextlib import closing
from datetime import date



# api = TqApi(TqSim(),web_gui=True)
acc = TqSim()
symbol = "SHFE.ni2007"
一跳价格 = 10
volume = 1#每次下单数
status = '等待开仓'
check_tick = 10
# open_Trade =
平仓时间='下午14:59:30-55秒'
# 委托远离几跳撤单 = 10
# 委托间隔多少秒撤单 = 120
# 保本损改变条件 = 20
止损 = 10#十跳止损
止盈 = 30#30跳止盈
波动开仓跳数 = 10
止损临时 = 0
委托订单=0
委托时间=0
挂多平单子列表=[]
多单价格列表=[]
挂空平单子列表=[]
空单价格列表=[]


'''
开盘前登录账户检查账户
开盘时间为晚上21:00:00
可以提前登录检查账户

多单怎么开仓
多单开仓按照最新卖一价＞前卖一价
需要判断当前价位有没有未平仓单
如果有，不开仓
多单怎么止盈
多单止盈为开仓价+1


空单怎么开仓
空单开仓按照最新买一价<前买一价
需要判断当前价位有没有未平仓单
如果有，不开仓
空单怎么止盈
空单止盈为最新价<开仓价止盈

以上开仓单量要互相持平最多的一边

如果涨停了怎么办
如果涨停在涨停价清仓(不能到涨停封板)
如果跌停了怎么办
如果跌停在跌停价清仓(不能到跌停封板)
一旦触发涨跌停价位，清仓后不再交易

如果账户资金使用完了怎么办
账户资金使用完，清仓重新开始

如果开盘价触及在涨跌停当天不再交易

每天最大多少回撤

每天出金多少
出金盈利的50％

实现程序化自动启动停止

实现自动选取最优网络环境

当一个方向止盈单未平完，再次遇到此价位，再次开仓和对象持平

每天下午14:59:30-55秒清仓'''



def start_trade(行情,ticks):#开仓判断
    global status,挂价订单,委托时间,对价订单

    if status == '等待开仓':
        oldt = max(ticks.last_price)
        newt = min(ticks.last_price)
        if oldt-newt != 0:
            status = '检测委托'
            # 止损临时 = '止损'
            委托时间 = ticks.datatime.tolist[-1]
            # if ticks.last_price[::-1].idmax()>ticks.last_price[::-1].idmin():
            if ticks.last_price[-1]<ticks.last_price[-2]:#

                对价订单 = api.insert_order(symbol, direction='BUY', offset='OPEN', volume=volume, limit_price=ticks.bid_price[-1])#对价做空

                挂价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSE', volume=volume,
                                        limit_price=ticks.bid_price[-1] - 一跳价格)

            else:
                对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume, limit_price=ticks.ask_price[-1])#对价做多
                挂价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='CLOSE', volume=volume,
                                        limit_price=ticks.bid_price[-1] - 一跳价格)  # 只做一单


def 开单检测(ticks):
    global status,挂空平单子列表,挂多平单子列表,空单价格列表,多单价格列表
    status = '正在运行'
    # a = api.get_order(对价订单['order_id'])
    data = api.get_position(symbol)
    多仓之和 = data['pos_long_today']
    空仓之和 = data['pos_short_today']
    # 委托价格1 = a['limit_price']
    # 未成交手数1 = a['volume_left']  # 单指此订单的为成交数量
    # 开单方向1 = a["direction"]
    # 下单时间 = a['insert_date_time']
    if ticks['bid_price1'].tolist()[-1] < ticks['bid_price1'].tolist()[-2]and (ticks['bid_price1'].tolist()[-1] not in 空单价格列表):#价格下跌且不在价格列表,正常
        print(ticks['bid_price1'].tolist()[-1],ticks['bid_price1'].tolist()[-2])
        if 多仓之和 > 空仓之和:#如果多仓持仓大于空仓,空仓补齐差额订单数量
            订单数量差 = 多仓之和 - 空仓之和
            对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
                                    limit_price=ticks['bid_price1'].tolist()[-1])  # 对价做空
            # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL

            挂价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSETODAY', volume=订单数量差,
                                    limit_price=ticks.bid_price1[-1] - 10*一跳价格)
            挂空平单子列表.append(挂价订单['order_id'])
            空单价格列表.append(挂价订单['limit_price'])
            print('dasda')
            return

        else:
            对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
                                    limit_price=ticks['bid_price1'].tolist()[-1])  # 对价做空
            # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL

            挂价订单 = api.insert_order(symbol=symbol, direction='BUY', offset='CLOSETODAY', volume=volume,
                                    limit_price=ticks['bid_price1'].tolist()[-1] - 一跳价格)#只做一单
            挂空平单子列表.append(挂价订单['order_id'])
            空单价格列表.append(挂价订单['limit_price'])
            return
    # if ticks['last_price'].tolist()[-1] < ticks['last_price'].tolist()[-2] and (ticks['bid_price1'].tolist()[-1] in 空单价格列表):#价格下跌且在价格列表,等待这一空单交易完成
    #     #获取当前价格已存在对应订单号,
    #     i=空单价格列表.index(ticks['bid_price1'])
    #
    #     a = api.get_order(挂空平单子列表[i]['order_id'])#获取当前价格已存在的空单
    #     print('空单价格列表:',i)
    #     #等待此订单号交易成功后下单,未成功不下单
    #     未成交手数1 = a['volume_left']  # 单指此订单的未成交数量
    #     if 多仓之和 > 空仓之和:#如果多仓持仓大于空仓,空仓补齐差额订单数量
    #         订单数量差 = 空仓之和 - 未成交手数1
    #         对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
    #                                 limit_price=ticks['bid_price1'].tolist()[-1])  # 对价做空
    #         # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL
    #
    #         挂价订单 = api.insert_order(symbol=symbol, direction='OPEN', offset='CLOSE', volume=订单数量差,
    #                                 limit_price=ticks['bid_price1'].tolist()[-1] - 一跳价格)
    #         挂多平单子列表.append(挂价订单['order_id'])
    #         多单价格列表.append(挂价订单['limit_price'])
    #         return
    #
    #     else:
    #         对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
    #                                 limit_price=ticks['bid_price1'].tolist()[-1])  # 对价做空
    #         # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL
    #
    #         挂价订单 = api.insert_order(symbol=symbol, direction='OPEN', offset='CLOSE', volume=volume,
    #                                 limit_price=ticks['bid_price1'].tolist()[-1] - 一跳价格)#只做一单
    #         挂多平单子列表.append(挂价订单['order_id'])
    #         多单价格列表.append(挂价订单['limit_price'])
    #         return
    if ticks['last_price'].tolist()[-1] > ticks['last_price'].tolist()[-2] :#and (ticks['ask_price1'].tolist()[-1] not in 多单价格列表):#价格上涨且不在价格列表,正常

        if 多仓之和 < 空仓之和:#如果多仓持仓小于空仓,空仓补齐差额订单数量
            订单数量差 = 空仓之和 - 多仓之和
            对价订单 = api.insert_order(symbol, direction='BUY', offset='OPEN', volume=volume,
                                    limit_price=ticks['ask_price1'].tolist()[-1])  # 对价做空
            # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL

            挂价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='CLOSETODAY', volume=订单数量差,
                                    limit_price=ticks['ask_price1'].tolist()[-1] - 一跳价格)
            挂多平单子列表.append(挂价订单['order_id'])
            多单价格列表.append(挂价订单['limit_price'])
            return

        else:
            对价订单 = api.insert_order(symbol, direction='BUY', offset='OPEN', volume=volume,
                                    limit_price=ticks['ask_price1'].tolist()[-1])  # 对价做空
            # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL

            挂价订单 = api.insert_order(symbol=symbol, direction='SELL', offset='CLOSETODAY', volume=volume,
                                    limit_price=ticks['ask_price1'].tolist()[-1] - 一跳价格)#只做一单
            挂多平单子列表.append(挂价订单['order_id'])
            多单价格列表.append(挂价订单['limit_price'])
            return
    # if ticks['last_price'].tolist()[-1] > ticks['last_price'].tolist()[-2] and (ticks['ask_price1'].tolist()[-1] in 空单价格列表):  # 价格上涨且在价格列表,等待这一空单交易完成
    #     # 获取当前价格已存在对应订单号,
    #     i = 空单价格列表.index(ticks['bid_price1'])
    #
    #     a = api.get_order(挂空平单子列表[i]['order_id'])  # 获取当前价格已存在的空单
    #     # 等待此订单号交易成功后下单,未成功不下单
    #     未成交手数1 = a['volume_left']  # 单指此订单的未成交数量
    #     if 多仓之和 > 空仓之和:  # 如果多仓持仓大于空仓,空仓补齐差额订单数量
    #         订单数量差 = 多仓之和 - 未成交手数1
    #         对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
    #                                 limit_price=ticks['ask_price1'].tolist()[-1])  # 对价做空
    #         # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL
    #
    #         挂价订单 = api.insert_order(symbol=symbol, direction='OPEN', offset='CLOSE', volume=订单数量差,
    #                                 limit_price=ticks['ask_price1'].tolist()[-1] - 一跳价格)
    #         挂多平单子列表.append(挂价订单['order_id'])
    #         多单价格列表.append(挂价订单['limit_price'])
    #         return
    #
    #     else:
    #         对价订单 = api.insert_order(symbol, direction='SELL', offset='OPEN', volume=volume,
    #                                 limit_price=ticks['ask_price1'].tolist()[-1])  # 对价做空
    #         # 当前价格 = ticks["ask_price1"].tolist()[-1]  # SELL
    #
    #         挂价订单 = api.insert_order(symbol=symbol, direction='OPEN', offset='CLOSE', volume=volume,
    #                                 limit_price=ticks['ask_price1'].tolist()[-1] - 一跳价格)  # 只做一单
    #         挂多平单子列表.append(挂价订单['order_id'])
    #         多单价格列表.append(挂价订单['limit_price'])
    #         return
def 固定止损止盈(ticks):
    global 止损临时,status
    # data=api.get_position(symbol)
    当前时间=ticks['datetime'].tolist()[-1]

    # if 当前时间 > 平仓时间:
    #     平所有(symbol)
    #     status = '终止交易'

def 平所有(symbol):#直接用
    data=api.get_position(symbol)
    多仓1=data['pos_long_his']
    多仓2=data['pos_long_today']
    空仓1=data['pos_short_his']
    空仓2=data['pos_short_today']

    if 多仓1!=0:
        api.insert_order(symbol=symbol, direction="SELL", offset="CLOSE", volume=多仓1)
    if 多仓2!=0:
        if symbol[:4]=="SHFE":
            api.insert_order(symbol=symbol, direction="SELL", offset="CLOSETODAY", volume=多仓2)
        else:
            api.insert_order(symbol=symbol, direction="SELL", offset="CLOSE", volume=多仓2)
    if 空仓1!=0:
        api.insert_order(symbol=symbol, direction="BUY", offset="CLOSE", volume=空仓1)
    if 空仓2!=0:
        if symbol[:4]=="SHFE":
            api.insert_order(symbol=symbol, direction="BUY", offset="CLOSETODAY", volume=空仓2)
        else:
            api.insert_order(symbol=symbol, direction="BUY", offset="CLOSE", volume=空仓2)

try:
    api = TqApi(acc,backtest=TqReplay(date(2020,5,13)),web_gui=True)
    ticks = api.get_tick_serial(symbol)
    # 行情 = api.get_tick_serial(symbol,60,100)
    while True:
        api.wait_update()
        print(status)
        # start_trade(ticks)
        开单检测(ticks)
        固定止损止盈(ticks)



except BacktestFinished as e:
    print(acc.trade_log)
    pass

api.close()

from tqsdk import TqApi,TargetPosTask,TqSim,InsertOrderTask,TqAccount
from contextlib import closing

api = TqApi(TqSim())

symbol = "SHFE.ni2007"  # 合约代码
# point = None
#start_price = 4247  # 起始价位
#grid_amount = 10  # 网格在多头、空头方向的格子(档位)数量
ticks = api.get_tick_serial(symbol)
target_pos = TargetPosTask(api, symbol)#创建目标持仓实例
insertOrder = InsertOrderTask(api,symbol, 'BUY', 'OPEN', 1)#下单实例
'''
direction (str): "BUY" 或 "SELL"
offset (str): "OPEN", "CLOSE" 或 "CLOSETODAY"
volume (int): 需要下单的手数
limit_price (float): [可选]下单价格, 默认市价单
order_chan (TqChan): [可选]委托单通知channel, 当委托单状态发生时会将委托单信息发到该channel上
trade_chan (TqChan): [可选]成交通知channel, 当有成交发生时会将成交手数(多头为正数，空头为负数)发到该channel上'''
target_volume = 0  # 目标持仓手数
# async def price_watcher(volume):
#     """该task在价格触发开仓价时开仓，触发平仓价时平仓"""
#     global target_volume
#
#     # global last_price2
#     # last_price2  = api.get_tick_serial()
#     # print(api.register_update_notify(ticks))
#     async with api.register_update_notify(ticks) as update_chan:  # 当 quote 有更新时会发送通知到 update_chan 上
#         while True:
#             async for _ in update_chan: # 当从 update_chan 上收到行情更新通知时判断是否触发开仓条件,此'_'为一个循环标志
#                 if (volume > 0 and ticks.iloc[-2].ask_price1 == ticks.iloc[-1].ask_price1):
#                     print('_____________')
#                     break
#                     chan = insertOrder._trade_chan(api,symbol,direction='BUY',offset='CLOSE',status='ACTIVE').is_online
#                 elif (volume > 0 and ticks.iloc[-2].ask_price1 > ticks.iloc[-1].ask_price1):#此时卖一价下跌,做空 or (volume < 0 and ticks.ask_price1 >= open_price):
#                     target_volume -= volume
#                     insertOrder._limit_price = ticks.iloc[-1].bid_price1#买一价
#                     print(insertOrder._limit_price)
#                     insertOrder._direction = 'SELL'
#                     insertOrder._offset = 'OPEN'
#                     insertOrder._volume = volume
#                     print("--------------------------------------")
#                     await insertOrder._run()#以单下划线开头的表示的是 protected 类型的变量，即保护类型只能允许其本身与子类进行访问，不能用于 from module import *
#                     print("时间:", ticks.iloc[-1].datetime, "最新价:", ticks.iloc[-1].ask_price1, "空开", volume, "手",)
#                     insertOrder._direction = 'BUY'
#                     insertOrder._offset = 'CLOSE'
#                     insertOrder._volume = volume
#                     insertOrder._limit_price = insertOrder._limit_price-10.0
#                     # insertOrder._limit_price = insertOrder._limit_price-point
#                     await insertOrder._run()
#                     print('空平价格:')
#                     print('账户资金:', api.get_account().balance, api.get_account().float_profit,)
#                     print('用户持仓信息:', api.get_position("DCE.pp2009"))
#                     print("时间:", ticks.iloc[-1].datetime, "最新价:", ticks.iloc[-1].ask_price1, "空平", volume, "手")
async def price_watcher2(volume):
    global target_volume
    async with api.register_update_notify(ticks) as update_chan:  # 当 quote 有更新时会发送通知到 update_chan 上
            while True:
                async for _ in update_chan:  # 当从 update_chan 上收到行情更新通知时判断是否触发开仓条件,此'_'为一个循环标志
                    if (volume > 0 and ticks.iloc[-2].ask_price1 == ticks.iloc[-1].ask_price1):
                        print('_____________')
                        break
                        chan = insertOrder._trade_chan(api, symbol, direction='BUY', offset='CLOSE',status='ACTIVE').is_online
                    elif (volume > 0 and ticks.iloc[-2].ask_price1 < ticks.iloc[-1].ask_price1):#此时卖一价上涨,做多 or (volume < 0 and quote.last_price < close_price):
                        target_volume += volume
                        insertOrder._limit_price = ticks.iloc[-1].ask_price1
                        insertOrder._direction = 'BUY'
                        insertOrder._offset = 'OPEN'
                        insertOrder._volume = volume
                        await insertOrder._run()
                        print("时间:", ticks.iloc[-1].datetime, "最新价:", ticks.iloc[-1].ask_price1, "买开", volume, "手",)
                        insertOrder._limit_price = insertOrder._limit_price+10.0
                        insertOrder._direction = 'SELL'
                        insertOrder._offset = 'CLOSE'
                        insertOrder._volume = volume
                        await insertOrder._run()
                        # target_volume -= volume
                        # target_pos.set_target_volume(target_volume)
                        print('账户资金:',api.get_account().balance,api.get_account().float_profit,)
                        print('用户持仓信息:',api.get_position("DCE.pp2009"))
                        print("时间:", ticks.iloc[-1].datetime, "最新价:", ticks.iloc[-1].ask_price1, "多平", volume, "手")


# api.create_task(price_watcher(1))
api.create_task(price_watcher2(1))


if __name__ == '__main__':
    with closing(api):  # 这个contextlib.closing()会帮它加上__enter__()和__exit__()，使其满足with的条件。
        while True:
            api.wait_update()
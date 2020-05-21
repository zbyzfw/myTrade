#%%
from tqsdk import TqApi, TqSim, TqBacktest,BacktestFinished,TqReplay,TargetPosTask
from datetime import date,datetime

api = TqApi(TqSim(),backtest=TqBacktest(start_dt=datetime(2020, 5, 12,21,1,2,795738,) ,end_dt=datetime(2020, 5, 13,14,59,59,0)),web_gui=True)

symbol = 'DCE.pp2009'
ticks = api.get_tick_serial(symbol)
quote = api.get_quote(symbol)
position = api.get_position(symbol)

status_now = '等待开仓'
status2_now ='等待开仓'

while True:
    api.wait_update()
    if api.is_changing(quote):
        print(status_now)
        if status_now == '等待开仓':
            if not position.pos_long:#多头持仓手数
                price1 = quote.bid_price1#买一价
                price2 = quote.ask_price1#卖一价
                open_position_long = api.insert_order(symbol=symbol,direction='BUY',offset='OPEN',volume=1,limit_price=price1)#
                status_now = '等待开仓成交'
        if status_now == '等待开仓成交':
            order = api.get_order(open_position_long.order_id)
            if order['volume_left'] == 0:
                status_now = '等待平仓'
        if status_now == '等待平仓':
            if  position.pos_long:
                close_position_long = api.insert_order(symbol=symbol,direction='SELL',offset='CLOSETODAY',volume=1,limit_price=price2)
                status_now = '等待平仓成交'
        if status_now == '等待平仓成交':
            order2 = api.get_order(close_position_long.order_id)
            if order2['volume_left'] == 0:
                status_now = '等待开仓'
        if status2_now == '等待开仓':
            if not position.pos_short:
                price1 = quote.bid_price1
                price2 = quote.ask_price1
                open_position_short = api.insert_order(symbol=symbol,direction='SELL',offset='OPEN',volume=1,limit_price=price2)
                status2_now = '等待开仓成交'
        if status2_now == '等待开仓成交':
            order3 = api.get_order(open_position_short.order_id)
            if order3['volume_left'] == 0:
                status2_now = '等待平仓'
        if status2_now == '等待平仓':
            if  position.pos_short:
                close_position_short = api.insert_order(symbol=symbol,direction='BUY',offset='CLOSETODAY',volume=1,limit_price=price1)
                status2_now = '等待平仓成交'
        if status2_now == '等待平仓成交':
            order4 = api.get_order(close_position_short.order_id)
            if order4['volume_left'] == 0:
                status2_now = '等待开仓'
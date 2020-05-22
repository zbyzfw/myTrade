from tqsdk import TqApi,TqSim,TqBacktest,BacktestFinished
import time
from datetime import date
acc = TqSim()
品种="CFFEX.IF1912"
一跳价格=0.2
一次下多少单子=1
当前状态="寻找开仓机会"
检测最近多少tick序列=10
波动开仓跳数=15
委托远离几条撤单=10
委托间隔多少秒撤单=120

保本损改变条件=20
止损=10
止盈=30

单根1分钟超过多少平仓=20

止损临时=0
委托单子=0
委托时间=0
def 开仓判断(行情,tick序列):
    global 委托单子,当前状态,止损临时,委托时间
    if 当前状态=="寻找开仓机会":
        mymax=max(tick序列['last_price'])
        mymin=min(tick序列['last_price'])
        print(mymax-mymin)
        if mymax-mymin>波动开仓跳数*一跳价格:
            当前状态="检测委托"
            止损临时=止损
            委托时间=tick序列['datetime'].tolist()[-1]
            if tick序列['last_price'][::-1].idxmax()>tick序列['last_price'][::-1].idxmin():
                委托单子 = api.insert_order(symbol=品种, direction="BUY", offset="OPEN", volume=一次下多少单子,limit_price=tick序列["bid_price1"].tolist()[-1])
            else:
                委托单子 = api.insert_order(symbol=品种, direction="SELL", offset="OPEN", volume=一次下多少单子,limit_price=tick序列["ask_price1"].tolist()[-1])

def 检测委托(行情,tick序列):
    global 委托单子,当前状态
    if 当前状态=="检测委托":
        a=api.get_order(委托单子['order_id'])
        委托价格1=a['limit_price']
        未成交手数1=a['volume_left']
        开单方向1=a["direction"]
        if 开单方向1=="BUY":
            当前价格=tick序列["bid_price1"].tolist()[-1]
        else:
            当前价格=tick序列["ask_price1"].tolist()[-1]
        下单时间=a['insert_date_time']
        if 未成交手数1==0:
            当前状态="等待平仓"
            print("已经开仓成功")
            return
        if abs(委托价格1-当前价格)>委托远离几条撤单*一跳价格:
            api.cancel_order(委托单子['order_id'])
            当前状态='寻找开仓机会'
            print("远离挂单,撤单了")
            print("委托价格",委托价格1)
            print("当前价格",当前价格)
            return 
        if (tick序列["datetime"].tolist()[-1]-委托时间)/1000000000 >委托间隔多少秒撤单:
            api.cancel_order(委托单子['order_id'])
            当前状态='寻找开仓机会'
            print("挂单太久,撤单了")
            return
def 持仓检测模块(行情,tick序列):
    global 止损临时
    data=api.get_position(品种)
    多仓之和=data['pos_long_his']+data['pos_long_today']
    多仓成本=data['open_price_long']
    空仓之和=data['pos_short_his']+data['pos_short_today']
    空仓成本=data['open_price_short']
    当前价格=tick序列["last_price"].tolist()[-1]
    if 多仓之和>0:
        if 当前价格>多仓成本+保本损改变条件*一跳价格:
            止损临时=0
    else:
        if 空仓成本>当前价格+保本损改变条件*一跳价格:
            止损临时=0
def 固定止损止盈(行情,tick序列):
    global 止损临时,当前状态
    data=api.get_position(品种)
    多仓之和=data['pos_long_his']+data['pos_long_today']
    多仓成本=data['open_price_long']
    空仓之和=data['pos_short_his']+data['pos_short_today']
    空仓成本=data['open_price_short']
    当前价格=tick序列["last_price"].tolist()[-1]
    if 多仓之和>0:
        if 当前价格>=多仓成本+止盈*一跳价格:
            平所有(品种)
            print(止盈)
            当前状态="寻找开仓机会"
        if 当前价格<=多仓成本-止损临时*一跳价格:
            平所有(品种)
            print(止损)
            当前状态="寻找开仓机会"
    else:
        if 当前价格<=空仓成本-止盈*一跳价格:
            平所有(品种)
            print(止盈)
            当前状态="寻找开仓机会"
        if 当前价格>=空仓成本+止损临时*一跳价格:
            平所有(品种)
            print(止损)
            当前状态="寻找开仓机会"
def 平所有(品种):
    data=api.get_position(品种)
    多仓1=data['pos_long_his']
    多仓2=data['pos_long_today']
    空仓1=data['pos_short_his']
    空仓2=data['pos_short_today']

    if 多仓1!=0:
        api.insert_order(symbol=品种, direction="SELL", offset="CLOSE", volume=多仓1)
    if 多仓2!=0:
        if 品种[:4]=="SHFE":
            api.insert_order(symbol=品种, direction="SELL", offset="CLOSETODAY", volume=多仓2)
        else:
            api.insert_order(symbol=品种, direction="SELL", offset="CLOSE", volume=多仓2)
    if 空仓1!=0:
        api.insert_order(symbol=品种, direction="BUY", offset="CLOSE", volume=空仓1)
    if 空仓2!=0:
        if 品种[:4]=="SHFE":
            api.insert_order(symbol=品种, direction="BUY", offset="CLOSETODAY", volume=空仓2)
        else:
            api.insert_order(symbol=品种, direction="BUY", offset="CLOSE", volume=空仓2)

def 一分钟检测(行情,tick序列):
    global 当前状态
    mymax=行情['high'].tolist()[-1]
    mymin=行情['low'].tolist()[-1]
    if mymax-mymin>单根1分钟超过多少平仓*一跳价格:
        平所有(品种)
        print("波动太大平仓")
        当前状态="寻找开仓机会"



def 平仓检测(行情,tick序列):
    global 当前状态
    if 当前状态=="等待平仓":
        持仓检测模块(行情,tick序列)
        固定止损止盈(行情,tick序列)
        #一分钟检测(行情,tick序列)







try:

    api=TqApi(acc, backtest=TqBacktest(start_dt=date(2019, 11, 1), end_dt=date(2019, 11, 5)))
    行情=api.获取K线(品种,60,100)
    tick序列=api.get_tick_serial(品种,检测最近多少tick序列)
    while True:
        api.wait_update()
        print(当前状态)
        开仓判断(行情,tick序列)
        检测委托(行情,tick序列)
        平仓检测(行情,tick序列)
except BacktestFinished as e:
  # 回测结束时会执行这里的代码
  print(acc.trade_log)
  pass
api.close()
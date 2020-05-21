#%%
from tqsdk import TqApi
import time
from pandas import Series
import pandas as pd
api = TqApi()
ticks = api.get_tick_serial("SHFE.ag2006")
quote = api.get_quote("SHFE.cu2006")
print(ticks)
print(ticks.iloc[-1].bid_price1)       # 最后一个Tick的买一价
S = Series(ticks.iloc[-1].datetime)
S = S.apply(str)
print(S)
# 0 时间戳
S = pd.to_datetime(S,unit='us',)
# print(S)
print(S)
# ticks.volume
# print(ticks.volume)
# ticks = api.get_tick_serial("SHFE.cu1812")
# while True: #通过wait_update刷新数据
#     api.wait_update()
#     print(quote.datetime)
#     print('_______________')
#     print(ticks.iloc[-1].bid_price1)
#%%
from pandas import Series,DataFrame
import pandas as pd
import time
from time import strftime
from datetime import datetime

timetamp = 1.5892108315e+18
timetamp =Series(timetamp)
print(timetamp)
# timetamp = pd.to_datetime(timetamp,format='%Y%m%d%H%M%S%f',errors='ignore')
# print(timetamp)
# timetamp = timetamp.apply(str)
timetamp = timetamp.apply(lambda x:int(x))
print(timetamp)
# timetamp = timetamp.apply(lambda x:str(x))
# timetamp = timetamp.str[0:13]
# timetamp = timetamp.apply(lambda x:int(x))
# print(timetamp)
timetamp = pd.to_datetime(timetamp,unit='ns').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
timetamp = timetamp.dt.strftime('%Y-%m-%d %H:%M:%S')

# timetamp = pd.to_datetime(timetamp,unit='s',errors='ignore').strftime('%Y%m%d%H%M%S')
# timetamp = timetamp.apply(lambda x:time.localtime(x))
print(timetamp)
# timetamp = timetamp.str[0:13].apply(lambda x: datetime.strptime(str(x),"%Y%m%d%H%M%S%f"))
# print(timetamp)

#%%
quote = api.get_quote("CZCE.SR009")
print(quote.last_price)
#
# while True:
#     api.wait_update()#是一个阻塞函数, 程序在这行上等待, 直到收到数据包才返回.
#     print (quote.datetime, quote.last_price)

#%%
klines = api.get_kline_serial("SHFE.cu2002", 10)#获取cu2002的十秒线,kiline是一个DataFrame对象
# while True:
#     api.wait_update()
#     print("最后一根K线收盘价", klines.close.iloc[-1])
print(klines.close.iloc[-1])
#%%
# 创建api实例，设置web_gui=True生成图形化界面
api = TqApi(web_gui=True)
# 订阅 cu2002 合约的10秒线
klines = api.get_kline_serial("SHFE.cu2002", 10)
while True:
    # 通过wait_update刷新数据
    api.wait_update()

#%%
account = api.get_account()
#要获得你交易账户中某个合约的持仓情况, 可以请求一个持仓引用对象:
position = api.get_position("DCE.m1901")
print("可用资金: %.2f" % (account.available))
print("今多头: %d 手" % (position.volume_long_today))
#发出一个委托单
order = api.insert_order(symbol="DCE.m1901", direction="BUY", offset="OPEN", volume=5, limit_price=3000)
print("委托单状态: %s, 已成交: %d 手" % (order.status, order.volume_orign - order.volume_left))
api.cancel_order(order)#撤销委托单
#%%
klines = api.get_kline_serial("DCE.m1901", 60)
while True:
    api.wait_update()
    if api.is_changing(klines):#判断指定对象是否以在最近一次的wait_update中被更新
        ma = sum(klines.close.iloc[-15:])/15
        print("最新价", klines.close.iloc[-1], "MA", ma)
        if klines.close.iloc[-1] > ma:
            print("最新价大于MA: 市价开仓")
            api.insert_order(symbol="DCE.m1901", direction="BUY", offset="OPEN", volume=5)

#%%
ticks = api.get_tick_serial("SHFE.cu1812")

ticks.iloc[-1].bid_price1       # 最后一个Tick的买一价
ticks.volume
#%%
import time
import datetime
print(time.time())
print(datetime.datetime.today())

print(datetime.datetime.now().year)
print(datetime.datetime.now().month)
print(datetime.datetime.now().day)
month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year
today = str(year)+str(month)+str(day)
print(today)
#%%

import os

path = os.getcwd()
print(path)
filelist = os.listdir(path)
# print(filelist)
for dir in filelist:
    dir = dir[7:]
    print(dir)
#%%
#写法1：
from tqsdk import TqApi
api = TqApi()
async with api.register_update_notify(order) as update_chan:
   async for _ in update_chan:
      if not order.is_online:
         break
## 执行…..

#写法2：

async with api.register_update_notify(order) as update_chan:
   while not order.is_online:
      await update_chan.recv()
## 执行…..

#想问一下 以上两种写法 是不是一样的？

#%%
print(datetime.datetime.fromtimestamp(klines.iloc[-1]["datetime"]/ 1e9))
#%%
import pandas as pd
import numpy as np
订单 = pd.DataFrame(columns=['symbol', '订单order_id', '买入方向direction', '持仓数volume_left','status',])
# df.iloc[0]=[1,2,3,4]
print(df)
已成交订单 = pd.DataFrame(columns=['symbol', '订单order_id', '买入方向direction', '持仓数volume_left','status',])

#取交集：
#pd.merge(df1,df2,on=['name', 'age', 'sex'],how='inner')
pd.merge(df1,df2,how='inner')
#取并集
#pd.merge(df1,df2,on=['name', 'age', 'sex'],how='outer')
pd.merge(df1,df2,how='outer')
#取差集（从df1中过滤df2中存在的数据）
df1 = df1.append(df2)
df1 = df1.append(df2)
df1 = df1.drop_duplicates(subset=['name', 'age', 'sex'],keep=False)
df1
#%%
import pandas as pd
# from .make_Ticks4 import 持仓检测模块

inp = [{'c1':10, 'c2':100}, {'c1':11,'c2':110}, {'c1':12,'c2':120}]
df = pd.DataFrame(inp)
df.drop()
print(df)

for a in df.itertuples(index=True, name='Pandas'):
    if a.c1 == 10:
        df.drop(a.index(0))
print(index)#, getattr(row, "c2"))
#%%

my_dict = {'子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
           '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
           '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'}

print('子' in my_dict.keys())
print('鼠' not in my_dict.values())

print('行初心' in my_dict.keys())
print('行初心' not in my_dict.values())
#%%
a = 3 - 1 in [1]
print(a)
'''
1 Lambda  #运算优先级最低
 2 逻辑运算符: or
 3 逻辑运算符: and
 4 逻辑运算符:not
 5 成员测试: in, not in
 6 同一性测试: is, is not
 7 比较: <,<=,>,>=,!=,==
 8 按位或: |
 9 按位异或: ^
10 按位与: &
11 移位: << ,>>
12 加法与减法: + ,-
13 乘法、除法与取余: *, / ,%
14 正负号: +x,-x'''
#%%
a={'aa8a9c1aa3d555ad5c430a06a766896c': 3449.0, 'b00a986500bbac6b48d343fbb203d05d': 3449.0}

print(3449.0 not in a.values())
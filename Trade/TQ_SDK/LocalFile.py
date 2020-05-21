#%%
from tqsdk import TqApi, TargetPosTask
from pandas import Series, DataFrame
import pandas as pd
import datetime
# SList = ['ag2006']
SList = ['ni2007','ag2006','rb2010','hc2010','fu2009','bu2006','ru2009',]#SHFE
DList = ['y2009','a2009','p2009','c2009','cs2009','jd2006','l2009','eg2009','pp2009','i2009','pg2011',]#CZCE
CList = ['SR009','FG009','TA009','MA009','RM009','AP010','CJ009']#

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year
today = str(year)+str(month)+str(day)

api = TqApi()


for SHFE in SList:
    globals()[SHFE] = api.get_tick_serial('SHFE.'+SHFE)
for CZCE in CList:
    globals()[CZCE] = api.get_tick_serial('CZCE.' + CZCE)
for DCE in DList:
    globals()[DCE] = api.get_tick_serial('DCE.' + DCE)
print("策略开始运行",globals()[SHFE].iloc[-1].datetime)
# def run():
while True:
    api.wait_update()
    for SHFE in SList:
        ASK = globals()[SHFE].iloc[-1].ask_price1#买一价
        BID = globals()[SHFE].iloc[-1].bid_price1#卖一价
        TIM = globals()[SHFE].iloc[-1].datetime
        TIM = Series(TIM)
        TIM = TIM.apply(lambda x:int(x))
        TIM = pd.to_datetime(TIM, unit='ns').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        TIM = TIM.dt.strftime('%Y-%m-%d %H:%M:%S')
        print(TIM)
        ASK = Series(ASK)
        BID = Series(BID)
        # TIM = Series(TIM)
        df = pd.DataFrame(list(zip(ASK, BID,TIM)))#多个series合并为dataFrame语法
        print(df)
        df.to_csv("./SHFE{0}{1}.csv".format(SHFE,today), encoding="utf-8-sig", mode="a", header=False, index=False)#文件名加上日期
    for CZCE in CList:
        ASK = globals()[CZCE].iloc[-1].ask_price1  # 买一价
        BID = globals()[CZCE].iloc[-1].bid_price1  # 卖一价
        TIM = globals()[CZCE].iloc[-1].datetime
        TIM = Series(TIM)
        TIM = TIM.apply(lambda x: int(x))
        TIM = pd.to_datetime(TIM, unit='ns').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        TIM = TIM.dt.strftime('%Y-%m-%d %H:%M:%S')
        print(TIM)
        ASK = Series(ASK)
        BID = Series(BID)
        # TIM = Series(TIM)
        df = pd.DataFrame(list(zip(ASK, BID, TIM)))  # 多个series合并为dataFrame语法
        print(df)
        df.to_csv("./CZCE{0}{1}.csv".format(CZCE,today), encoding="utf-8-sig", mode="a", header=False, index=False)#'a'为增加模式,不写入header和index
        # BID.to_csv("./{}.csv".format(SYMBOL), encoding="utf-8-sig", mode="a", header=False, index=False)
    for DCE in DList:
        ASK = globals()[DCE].iloc[-1].ask_price1  # 买一价
        BID = globals()[DCE].iloc[-1].bid_price1  # 卖一价
        TIM = globals()[DCE].iloc[-1].datetime
        TIM = Series(TIM)
        TIM = TIM.apply(lambda x: int(x))
        TIM = pd.to_datetime(TIM, unit='ns').dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        TIM = TIM.dt.strftime('%Y-%m-%d %H:%M:%S')
        print(TIM)
        ASK = Series(ASK)
        BID = Series(BID)
        # TIM = Series(TIM)
        df = pd.DataFrame(list(zip(ASK, BID, TIM)))  # 多个series合并为dataFrame语法
        print(df)
        df.to_csv("./DCE{}{1}.csv".format(DCE,today), encoding="utf-8-sig", mode="a", header=False, index=False)


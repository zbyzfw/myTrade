#%%
from pandas import Series,DataFrame
import pandas as pd
import sys, os

today = input('输入日期')
path = os.getcwd()
filelist = os.listdir(path)
for dir in filelist:
    dir = dir[7:]
    ticks = pd.read_csv(r'{0}{1}'.format(today,dir))
# print(ticks)
    S = ticks.iloc[:,1]
# S = ask_price1.head(90)
# print(S)
# ask_price1 = ask_price1.apply(lambda x:max(x))
# print(ask_price1)
    print('{0}日{1}商品的tick总数{2}'.format(today,dir,S.count()))
# print(S.iloc[1])
# print(ask_price1.describe())
# i = 1
    sys.setrecursionlimit(S.count()+10)#
    i=1
    a=0
    def ticksCount(i,a,):
        if i == S.count()-1:
            # if df3.iloc(i,1) == df3.iloc(i+1,1)
            return a
        else:
            if  S.iloc[i] == S.iloc[i+1]:
            # a +=1
                return ticksCount(i+1,a)
            else:
                return ticksCount(i+1,a+1)
    print('波动次数',a)
# print(ticksCount(1,0,))

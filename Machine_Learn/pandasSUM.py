#%%
#下跌次数,上涨次数,变化次数
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
df3 = DataFrame([[1, 2, 3], [4, 5, np.nan], [7, 8, 9]], index=['A', 'B', 'C'], columns=['c1', 'c2', 'c3'])
print(df3)
'''
   c1  c2   c3
A   1   2  3.0
B   4   5  NaN
'''
# 按照每一列　相加，返回　
print(df3.sum())
#　指定　axis, 按照每一行相加
print(df3.sum(axis=1))

print(df3.min())
print(df3.min(axis=1))
#%%
print(df3.mean())

# 打印出dataframe的数学信息包含count,mean,std,min,max,...
print(df3.describe())
#%%
#递归和迭代
# i = 1
# def count():
#     if i > df3.count():
#         # if df3.iloc(i,1) == df3.iloc(i+1,1)
#         return
#     else:
#         # if  df3.iloc(i,1) == df3.iloc(i+1,1):
#             # return i = i+1
#         else:
#             print(a)
#             # return normal_recursion(i=i+1,a=a+1)
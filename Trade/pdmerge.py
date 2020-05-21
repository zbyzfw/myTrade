import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
"""
pd表的合并示例
left - 一个DataFrame对象。
right - 另一个DataFrame对象。
on - 列(名称)连接，必须在左和右DataFrame对象中存在(找到)。
left_on - 左侧DataFrame中的列用作键，可以是列名或长度等于DataFrame长度的数组。
right_on - 来自右的DataFrame的列作为键，可以是列名或长度等于DataFrame长度的数组。
left_index - 如果为True，则使用左侧DataFrame中的索引(行标签)作为其连接键。 
在具有MultiIndex(分层)的DataFrame的情况下，级别的数量必须与来自右DataFrame的连接键的数量相匹配。
right_index - 与右DataFrame的left_index具有相同的用法。
how - 它是left, right, outer以及inner之中的一个，默认为内inner(合并后删除多余的字段)。 下面将介绍每种方法的用法。
sort - 按照字典顺序通过连接键对结果DataFrame进行排序。默认为True，设置为False时，在很多情况下大大提高性能。
"""
w1 = pd.read_csv("./1.csv")#读取csv文件
#读取四张表,分别是用户表,商品表,订单表,付款表
#合并这些表,操作类似于数据库
_mg = pd.merge(w1,w2,how='inner',on=['product_id','product_id'])#在w1,w2中按product_id进行合并,类似于数据库中的外键
mt = pd.merge(_mg,w3,on=['orde_id','order_id'])#在按order_id合并第三张表

mt.head(10)

cross = pd.crosstab(mt['user_id'],mt['aisle'])



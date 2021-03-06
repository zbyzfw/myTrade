R-Breaker 是一种短线日内交易策略，它结合了趋势和反转两种交易方式。该策略也长期被Future Thruth 杂志评为最赚钱的策略之一，尤其在标普500 股指期货上效果最佳。该策略的主要特点如下：

第一、根据前一个交易日的收盘价、最高价和最低价数据通过一定方式计算出六个价位，从大到小依次为突破买入价、观察卖出价、反转卖出价、反转买入价、观察买入价和突破卖出价，以此来形成当前交易日盘中交易的触发条件。通过对计算方式的调整，可以调节六个价格间的距离，进一步改变触发条件。

第二、根据盘中价格走势，实时判断触发条件，具体条件如下：

当日内最高价超过观察卖出价后，盘中价格出现回落，且进一步跌破反转卖出价构成的支撑线时，采取反转策略，即在该点位（反手、开仓）做空；
当日内最低价低于观察买入价后，盘中价格出现反弹，且进一步超过反转买入价构成的阻力线时，采取反转策略，即在该点位（反手、开仓）做多；
在空仓的情况下，如果盘中价格超过突破买入价，则采取趋势策略，即在该点位开仓做多；
在空仓的情况下，如果盘中价格跌破突破卖出价，则采取趋势策略，即在该点位开仓做空。
第三、设定止损以及止盈条件；

第四、设定过滤条件；

第五、在每日收盘前，对所持合约进行平仓。

具体来看，这六个价位形成的阻力和支撑位计算过程如下：

观察卖出价 = High + 0.35 * (Close – Low)
观察买入价 = Low – 0.35 * (High – Close)
反转卖出价 = 1.07 / 2 * (High + Low) – 0.07 * Low
反转买入价 = 1.07 / 2 * (High + Low) – 0.07 * High
突破买入价 = 观察卖出价 + 0.25 * (观察卖出价 – 观察买入价)
突破卖出价 = 观察买入价 – 0.25 * (观察卖出价 – 观察买入价)
其中，High、Close、Low 分别为昨日最高价、昨日收盘价和昨日最低价。这六个价位从大到小一次是，突破买入价、观察爱出价、反转卖出价、反转买入价、观察买入价和突破卖出价。
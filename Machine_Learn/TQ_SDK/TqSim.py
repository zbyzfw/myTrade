#%%
from tqsdk import TqApi,TqSim,TargetPosTask
'''
开盘:卖一价涨,做多

卖一价涨,做多
平仓:成交之后再挂一点(一个价差),止盈(单子卖出),
止盈单成交以后,开最新的卖一价的多单,判断,反向单持仓单量,多单空单持平

买一价跌,做空
平仓

下午两点59分30秒,清仓
'''
api = TqApi(TqSim())
# 设置 rb1810 持仓为多头5手
target_pos = TargetPosTask(api, "SHFE.rb1810")
target_pos.set_target_volume(5)
while True:
    # 需在 set_target_volume 后调用wait_update()以发出指令
    api.wait_update()
# order = api.insert_order(symbol="SHFE.ag2006", direction="BUY", offset="OPEN", limit_price=4310, volume=2)
# print(order)
account = api.get_account()#资金情况
print(account)
print(api.get_position()) #持仓情况
while order.status != "FINISHED":
    api.wait_update()
    print("委托单状态: %s, 未成交手数: %d 手" % (order.status, order.volume_left))
#%% 多个合约和多个账户

import argparse
from tqsdk import TqApi, TqSim, TqAccount

#解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--broker')#交易所名称
parser.add_argument('--user_name')
parser.add_argument('--password')
parser.add_argument('--symbol')#交易商品号
args = parser.parse_args()
print("策略参数为: ", args.user_name, args.symbol)

api = TqApi(TqAccount(args.broker, args.user_name, args.password))
# 开仓两手并等待完成
order = api.insert_order(symbol=args.symbol, direction="BUY", offset="OPEN", limit_price=4310,volume=2)
while order.status != "FINISHED":
    api.wait_update()
print("已开仓")
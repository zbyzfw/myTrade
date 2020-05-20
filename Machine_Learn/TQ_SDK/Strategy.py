'''
双均线策略
'''
from tqsdk import TqApi, TqSim, TargetPosTask
from tqsdk.tafunc import ma

SHORT = 30
LONG = 60
SYMBOL = "SHFE.bu1912"

api = TqApi(TqSim())

data_length = LONG + 2
klines = api.get_kline_serial(SYMBOL, duration_seconds=60, data_length=data_length)
target_pos = TargetPosTask(api, SYMBOL)

while True:
    api.wait_update()

    if api.is_changing(klines.iloc[-1], "datetime"):  # 产生新k线:重新计算SMA
        short_avg = ma(klines.close, SHORT)  # 短周期
        long_avg = ma(klines.close, LONG)  # 长周期

        # 均线下穿，做空
        if long_avg.iloc[-2] < short_avg.iloc[-2] and long_avg.iloc[-1] > short_avg.iloc[-1]:
            target_pos.set_target_volume(-3)
            print("均线下穿，做空")

        # 均线上穿，做多
        if short_avg.iloc[-2] < long_avg.iloc[-2] and short_avg.iloc[-1] > long_avg.iloc[-1]:
            target_pos.set_target_volume(3)
            print("均线上穿，做多")
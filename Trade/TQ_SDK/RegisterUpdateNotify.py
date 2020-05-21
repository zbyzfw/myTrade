'''
register_update_notify(obj: Optional[Any] = None, chan: Optional[tqsdk.channel.TqChan] = None) → tqsdk.channel.TqChan
注册一个channel以便接受业务数据更新通知

调用此函数将返回一个channel, 当obj更新时会通知该channel

推荐使用 async with api.register_update_notify() as update_chan 来注册更新通知

如果直接调用 update_chan = api.register_update_notify() 则使用完成后需要调用 await update_chan.close() 避免资源泄漏

Args:
obj (any/list of any): [可选]任意业务对象, 包括 get_quote 返回的 quote, get_kline_serial 返回的 k_serial, get_account 返回的 account 等。默认不指定，监控所有业务对象

chan (TqChan): [可选]指定需要注册的channel。默认不指定，由本函数创建

Example:


'''

# 获取 SHFE.cu1812 合约的报价
from tqsdk import TqApi

async def demo():
    quote = api.get_quote("SHFE.cu1812")
    async with api.register_update_notify(quote) as update_chan:
        async for _ in update_chan:
            print(quote.last_price)

api = TqApi()
api.create_task(demo())
while True:
    api.wait_update()

#以上代码将输出
nan
51850.0
51850.0
51690.0
...
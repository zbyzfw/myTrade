import random
import asyncio


async def random_number_gen(delay, start, end):
    while True:
        #循环执行时，每次循环都会执行函数内部的代码，执行到 yield XXX 时，函数就返回一个迭代值，下次迭代时，代码从 yield XXX 的下一条语句继续执行，
        yield random.randint(start, end)#yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，
        await asyncio.sleep(delay)

async def main():
    async for i in random_number_gen(1, 0, 100):
        print(i)


try:
    print("Starting to print out random numbers...")
    print("Shut down the application with Ctrl+C")
    asyncio.run(main())
except KeyboardInterrupt:
    print("Closed the main loop..")
import time
import asyncio
import sys


A = [i.strip() for i in sys.stdin.readlines()]

stops = []
cnt = 1
for i in A:
    if not i:
        break
    stops.append([cnt] + list(map(int, i.split())))
    cnt += 1
A = A[A.index('') + 1:]

products = []
for i in A:
    if i:
        f = i.split()
        products.append([f[0]] + [sum(map(int, f[1:]))])


async def gift(name, time):
    print(f'Buy {name}')
    await asyncio.sleep(time / 100)
    print(f'Got {name}')


async def shop(num, stop_time, duration_trip):
    global products

    print(f'Buying gifts at {num} stop')
    shop_time = stop_time
    if products:
        products_ = products.copy()
        A = []
        while stop_time and products_:
            max_el = max(products_, key=lambda x: x[1])
            del products_[products_.index(max_el)]
            if max_el[1] <= stop_time:
                A.append(max_el)
                del products[products.index(max_el)]
                stop_time -= max_el[1]

        tasks = [
            asyncio.create_task(gift(*i))
            for i in A
        ]
        await asyncio.gather(*tasks)
        for i in A:
            shop_time -= i[1]

    time.sleep((stop_time - shop_time) / 100)
    print(f'Arrive from {num} stop')
    time.sleep(duration_trip / 100)


for i in stops:
    asyncio.run(shop(*i))


if products:
    for i in products:
        asyncio.run(gift(*i))


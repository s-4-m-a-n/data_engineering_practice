import asyncio
from os import PRIO_PGRP
import aiohttp
import time

def get_task(session, params_collections, fake_url=True):
    tasks = []
    API = 'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input'

    if fake_url:
        fUrls = [
            "https://www.fakeurl.com.np/?ajax=true&from=input",
            'https://www.daraz.com.np/groceries-canned-dry-packaged-food/?ajax=true&from=input'
        ]

        for furl in fUrls:
            task = asyncio.create_task(session.get(furl))
            task.name = furl
            task.status = 'fake'
            tasks.append(task)

    for params in params_collections:
        query_str = f"&page={params['page']}&q={params['q']}"
        full_url = API + query_str

        task = asyncio.create_task(session.get(full_url))
        task.name = full_url
        task.status = 'not fake'

        tasks.append(task)

    return tasks

async def main(params_collections):
    
    """ execute multiple api call asynchronously using gather()"""

    async with aiohttp.ClientSession() as session:
        tasks = get_task(session, params_collections)
        done, pending = await asyncio.wait(tasks)

        #  display output
        for response in done:
            print(f"URL: {response.name}")
            print(f"status: {response.status}")

            data = None
            if not response.exception():
                data = await response.result().text()
                print("status code : ", response.result().status)
                data = data[:10]

            print(f"data: {data}")
            print("\n")
            
        for task in pending:
            print(f"pending_task = {task.name}")
        
start = time.time()

params_collections = [
        {
            'page': 1,
            'q': 'nuts'
        },
        {
            'page': 2,
            'q': 'nuts'
        }
]

asyncio.run(main(params_collections))

print(f"execution time : {time.time() - start} ")
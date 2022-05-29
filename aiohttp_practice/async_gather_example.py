import asyncio
import aiohttp
import time

def get_task(session, params_collections):
    tasks = []
    API = 'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input'
    for params in params_collections:
        tasks.append(session.get(API, params=params))
    return tasks

async def main(params_collections):
    """ execute multiple api call asynchronously using gather()"""
    
    async with aiohttp.ClientSession() as session:
        tasks = get_task(session,params_collections)
        responses = await asyncio.gather(*tasks)
        
        #display output
        for response in responses:
            print(f"URL: {response.url}")
            print(f"status :{response.status}")

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
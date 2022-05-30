import asyncio
import aiohttp
import time

def get_task(session, params_collections, fake_url=True):
    tasks = []
    API = 'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input'

    if fake_url:
        fUrl = "https://www.fakeurl.com.np/?ajax=true&from=input"
        tasks.append(asyncio.create_task(session.get(fUrl), name=fUrl))

    for params in params_collections:
        query_str = f"&page={params['page']}&q={params['q']}"
        full_url = API + query_str

        tasks.append(asyncio.create_task(session.get(full_url), name=full_url))

    return tasks

async def main(params_collections):
    
    """ execute multiple api call asynchronously using gather()"""

    async with aiohttp.ClientSession() as session:
        tasks = get_task(session, params_collections)
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        #  display output
        for index, response in enumerate(responses):
            if isinstance(response, Exception):
                exception_task = tasks[index]
                print(f"URL: {exception_task.get_name()}")
            else:
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
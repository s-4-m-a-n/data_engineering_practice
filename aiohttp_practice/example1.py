import asyncio
import aiohttp
import time
import ujson

"""
a basic example of asynchronous API call using aiohttp
"""

# API = 'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input&page={page}&q=nuts'

async def main(params, timeout):
    #preparing API
    API = 'https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input'

    #create session and perform asynchronous api call
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
       
            response = await session.get(API, params = params)
            print(f"URL: {response.url}")
            print(f"status :{response.status}")
            print(f"header : {response.headers}")
            text = await response.text()
        
            print("body: ",text[:20])
            
    except Exception as e:
        print(f"{e} Session timeout")
            
start = time.time()

# loop  = asyncio.get_event_loop()
# loop.run_until_complete(main(1))  # does routing check
# or we can simply use asyncio.run()
params = {
    'page': 1,
    'q': 'nuts'
}
timeout = aiohttp.ClientTimeout(total=7)  # if total=2 then we will get TimeoutError
asyncio.run(main(params, timeout))
print(f"execution time: {time.time() - start} s")

        
import aiohttp
import asyncio
import time

def get_tasks(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(session.get(url))
        task.name = url
        tasks.append(task)
    return tasks


async def scraper(urls):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, urls)
        done, pending = await asyncio.wait(tasks)

        for task in done:
            print("completed task")
            print(f"url:{task.name}")

            if task.exception():
                print("status code : exception occurred")
            else:
                print(f"status code: {task.result().status}")
            
        for task in pending:
            print("pending tasks")
            print(f"url: {task.name}")



start = time.time()
for i in range(5):
    iter_start = time.time()
    url1 = f"https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input&page={2*i}&q=nuts"
    url2 = f"https://www.daraz.com.np/groceries-canned-dry-packaged-food-dried-goods-dried-fruit-nuts/?ajax=true&from=input&page={2*i+1}&q=nuts"
    asyncio.run(scraper([url1, url2]))
    print(f"iter execution time: {time.time() - iter_start}s\n")
print(f"execution time: {time.time() - start}s")

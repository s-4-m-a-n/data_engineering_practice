import asyncio

import time

async def main():
	print("before sleep")
	task = asyncio.create_task(show())
	await asyncio.sleep(2)
	print("after sleep")
	r = await task
	print(r)
	
async def show():
	print("zzzzzzzz")
	await asyncio.sleep(1)
	print("hello world")
	return 1
    

#asyncio.run(main())
async def run():
	await asyncio.gather(main(),main())

asyncio.run(run())

import asyncio


# 1. Define the coroutine
async def main():
    print("Hello...")
    # asyncio.sleep simulates a network delay (like fetching a webpage)
    await asyncio.sleep(2)
    print("...World!")


# 2. Run the coroutine
asyncio.run(main())
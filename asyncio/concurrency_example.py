import asyncio
import time


async def fetch_data(id, delay):
    print(f"Task {id}: Fetching data...")
    await asyncio.sleep(delay)  # Simulating a slow network request
    print(f"Task {id}: Data received!")
    return f"Data {id}"


async def main():
    start_time = time.time()

    # asyncio.gather fires them all off at the same time
    results = await asyncio.gather(
        fetch_data(1, 2), fetch_data(2, 3), fetch_data(3, 1)
    )

    print(f"All data fetched: {results}")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")


asyncio.run(main())
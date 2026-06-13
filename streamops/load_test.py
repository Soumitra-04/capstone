import sys
import asyncio
import httpx
import time
import argparse
import random
import uuid
from collections import Counter

# Prevent 'Event loop is closed' errors on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def background_growth(client):
    """Slowly grow the database randomly when load test runs."""
    choice = random.randint(1, 3)
    base_url = "http://localhost:5174/api"
    try:
        if choice == 1:
            username = f"user_{uuid.uuid4().hex[:8]}"
            await client.post(f"{base_url}/users/register", json={"username": username, "email": f"{username}@test.com", "password": "pw"})
        elif choice == 2:
            game_name = f"Game {uuid.uuid4().hex[:6]}"
            await client.post(f"{base_url}/games", json={"name": game_name, "description": "Load test game"})
        elif choice == 3:
            await client.post(f"{base_url}/streams", json={"streamer_id": f"streamer_{uuid.uuid4().hex[:4]}", "title": f"Live {uuid.uuid4().hex[:4]}!"})
    except Exception:
        pass

async def fetch(client, url, semaphore, results):
    """Fetch a single URL and record the result status."""
    async with semaphore:
        try:
            if random.random() < 0.05:
                asyncio.create_task(background_growth(client))
                
            response = await client.get(url)
            results[response.status_code] += 1
        except Exception as e:
            results[type(e).__name__] += 1

async def hammer(url, count=100, concurrency=20):
    """Run the load test with a specified concurrency limit."""
    print(f"Starting load test on {url} with {count} requests (concurrency: {concurrency})...")
    
    # Use a semaphore to strictly enforce the concurrency limit
    semaphore = asyncio.Semaphore(concurrency)
    results = Counter()
    
    start_time = time.time()
    
    # Using limits parameter to increase the connection pool size
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency)
    
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [fetch(client, url, semaphore, results) for _ in range(count)]
        await asyncio.gather(*tasks)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Print statistics
    print("\n" + "="*30)
    print("--- Load Test Results ---")
    print("="*30)
    print(f"Target URL:        {url}")
    print(f"Total Requests:    {count}")
    print(f"Concurrency Level: {concurrency}")
    print(f"Time Taken:        {duration:.2f} seconds")
    print(f"Requests/Second:   {count / duration:.2f} req/s")
    print("\nStatus Codes/Errors:")
    for status, status_count in sorted(results.items(), key=lambda x: str(x[0])):
        print(f"  [{status}]: {status_count}")
    print("="*30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async Load Tester")
    parser.add_argument("--url", type=str, default="http://localhost:8001/streams", help="Target URL")
    parser.add_argument("-c", "--count", type=int, default=500, help="Total number of requests to send")
    parser.add_argument("-n", "--concurrency", type=int, default=50, help="Maximum number of concurrent requests")
    
    args = parser.parse_args()
    
    # Run the async event loop
    try:
        asyncio.run(hammer(args.url, count=args.count, concurrency=args.concurrency))
    except KeyboardInterrupt:
        print("\nLoad test interrupted by user.")

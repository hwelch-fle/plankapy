from itertools import batched
from typing import Any
from plankapy.v2.api import AsyncPlankaEndpoints, PlankaEndpoints
from httpx import AsyncClient, Client, Limits
import asyncio

from time import perf_counter

sync_client = Client(base_url='http://192.168.90.250:1337', limits=Limits(max_connections=100))
sync_planka = PlankaEndpoints(sync_client)


async_client = AsyncClient(base_url='http://192.168.90.250:1337', limits=Limits(max_connections=100))
async_planka = AsyncPlankaEndpoints(async_client)

def sync_auth():
    tok = sync_planka.createAccessToken(emailOrUsername='demo', password='demo')['item']
    sync_planka.client.headers['Authorization'] = f'Bearer {tok}'
     
async def async_auth():
    r = await async_planka.createAccessToken(emailOrUsername='demo', password='demo')
    tok = r['item']
    async_planka.client.headers['Authorization'] = f'Bearer {tok}'

async def get_projects():
    await async_auth()
    results: list[Any] = []
    
    try:
        tasks = [async_planka.getProjects() for _ in range(1000)]
        for batch in batched(tasks, n=20):
            results.extend(await asyncio.gather(*batch, return_exceptions=True))
        return results
    finally:
        await async_planka.deleteAccessToken()

if __name__ == '__main__':
    # Dispatch 100 async requests
    s = perf_counter()
    vals = asyncio.run(get_projects())
    e = perf_counter()
    print(f'Async: {e-s:.2f}s')
    print(len([v for v in vals if not isinstance(v, Exception)]), ' Successful')
    if isinstance(vals[0], Exception):
        print(vals[0])
    
    # Dispatch 100 sync requests
    s = perf_counter()
    sync_auth()
    vals: list[Any] = []
    for i in range(1000):
        try:
            vals.append(sync_planka.getProjects())
        except Exception:
            pass
    sync_planka.deleteAccessToken()
    e = perf_counter()
    print(f'Sync: {e-s:.2f}s')
    print(len(vals), ' Successful')
import aiohttp
import asyncio
from aiohttp import ClientSession
import json



loop = asyncio.get_event_loop()
loop.run_until_complete(fetch())
loop.close()
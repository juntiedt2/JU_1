#!/usr/bin/env python

import asyncio
import websockets
import os.path
from RedisQueue import RedisQueue

async def UniPi_ws():
    async with websockets.connect('ws://10.0.0.52/ws') as websocket:
        while True:
            if os.path.isfile("/home/pi/eng-env/webapp/stop_server.txt"):
                break         
            message = await websocket.recv()
            #print(message)
            if not "temp" in message:
                q.put(message)

if __name__ == '__main__':
    print("UniPi_ws_client started")
    q = RedisQueue('ws_1')
    asyncio.get_event_loop().run_until_complete(UniPi_ws())
    print("UniPi_ws_client stopped")
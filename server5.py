#!/usr/bin/env python

# UniPi Python Control Panel
# UniPi_server5.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 24.03.2018

import sys
import json
import asyncio
import engineio
from aiohttp import web
from asyncio_redis import RedisProtocol
from web_init_class import *

eio = engineio.AsyncServer(async_mode='aiohttp')
app = web.Application()
eio.attach(app)
wi = web_init("10.0.0.52","8080")              # Raspberry running UniPi-evok

clients = []
user_event = {'event':'users', 'uc':0}
transport = None

async def index(request):
    with open('./templates/simple.html') as f:
        return web.Response(text=f.read(), content_type='text/html')
        
async def broadcast(data):
    global clients
    if type(data) == 'str':
        payload = json.loads(data) 
    payload = (data)
    for client in clients:
        #print("message to client: ", client, payload, type(payload)) 
        print("server out ", len(clients))        
        await eio.send(client, payload, binary=False)
        
async def update_users():
    global clients
    global user_event
    print("update_users")
    user_event['uc'] = len(clients)
    payload = user_event
    await broadcast(user_event) 

async def redis_read():
    global loop
    global transport
    transport, protocol = await loop.create_connection(RedisProtocol, 'localhost', 6379)
    while True:
        len = await protocol.llen('queue:ws_2')
        if len > 0:
            data = await protocol.lpop('queue:ws_2')
            if "close" in data:
                break
            data = eval(data)
            #print("input from Redis: ", data, type(data))
            #print("                              redis in")
            await broadcast(data)
            #await asyncio.sleep(0)
    print("-------> redis_read loop beendet <-------")        
    transport.close()
    sys.exit(0)    

async def redis_write(message):
    global loop
    transport, protocol = await loop.create_connection(RedisProtocol, 'localhost', 6379)
    #print("output to Redis: ", message)
    #print("                              redis out")
    await protocol.rpush('queue:ws_3', [message])
    transport.close()
    
@eio.on('connect')
async def connect(sid, environ):
    global clients
    clients.append(sid)
    print("connect ", sid)
    payload = wi.get_init_data()
    #print(payload, type(payload))
    await eio.send(sid, payload, binary=False)
    await update_users()        
 
@eio.on('message')
async def message(sid, data):
    global clients
    await redis_write(data)
    print("           server in ", (clients.index(sid)+1))    
    #data = eval(data)
    #print('message from client: ', sid, data, type(data))

@eio.on('disconnect')
def disconnect(sid):
    global clients
    #print('disconnect ', sid)
    clients.remove(sid)
    upd_users = asyncio.ensure_future(update_users()) 
 

app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    global loop
    loop = asyncio.get_event_loop()
    redis_reader = asyncio.ensure_future(redis_read())     
    web.run_app(app)
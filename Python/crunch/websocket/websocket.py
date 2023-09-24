import asyncio
import functools
import json
import os
import socket
from datetime import datetime

import pandas as pd
import websockets
from watchgod import awatch

import crunch.util as util


async def watcher(queue):
    """
    param: queue
    type queue: asyncio queue
    watches for changes in the output folder, 
    and puts them in the asyncio queue
    """
    if not os.path.exists("crunch/output"):
        os.makedirs("crunch/output")
    async for changes in awatch('./crunch/output/'):
        for a in changes:
            file_path = a[1]
            # get last row of changed file
            df = pd.read_csv(file_path).iloc[-1]
            # format how we send it to frontend
            time = datetime.fromtimestamp(int(df.time)).strftime("%H:%M:%S")
            data = {"name": file_path[16:-4], "value": df.value, "time": time}
            # put it queue so web socket can read
            await queue.put([data])


async def handler(websocket, path, queue):
    try:
        while True:
            data = await queue.get()
            await websocket.send(json.dumps(data))
    finally:
        print("Lost connection with websocket client")


def start_websocket():
    """
    Starts the websocket and initializes an asyncio queue 
    which we can put items into to send them over the websocket
    """
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)

    local_ip = socket.gethostbyname(socket.gethostname())
    ip = "127.0.0.1" if util.config("websocket", "use_localhost") == "True" else local_ip
    port = int(util.config("websocket", "port"))

    print("##################################################################")
    print("###### Paste the websocket ip on the frontend to connect")
    print("###### IP: ", ip)
    print("###### Port: ", port)
    print("##################################################################")

    start_server = websockets.serve(functools.partial(handler, queue=queue), ip, port)
    loop.run_until_complete(asyncio.gather(
        start_server,
        watcher(queue),
    ))

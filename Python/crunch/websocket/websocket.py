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
from SimpleARIMAForecasting import establish_reference, predict_next_direction


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
            baseline_items = 10
            df = pd.read_csv(file_path)

            # get last 10 rows of changed file
            print("10 last: ",df.iloc[-10:,1].values.astype(float))
            if len(df.index)+1>=baseline_items:
                mean, std = establish_reference(df.iloc[1:baseline_items,1].values.astype(float))
                prediction = predict_next_direction(df.iloc[-10:,1].values.astype(float),mean,std)
                print("Prediction: ", prediction)
                # put it queue so web socket can read
                await queue.put({"message": str(prediction)})


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
    queue = asyncio.Queue()

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

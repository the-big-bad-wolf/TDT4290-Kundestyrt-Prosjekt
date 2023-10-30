import asyncio
import functools
import json
import os
import socket
import pandas as pd
from crunch.forecasting.cognitive_load_predictor import CognitiveLoadPredictor
import websockets
from watchgod import awatch
import crunch.util as util


class WebSocketServer:
    def __init__(self):
        self.predictor = None

    async def watcher(self, queue):
        if not os.path.exists("crunch/output"):
            os.makedirs("crunch/output")

        baseline_items = int(util.config("websocket", "baseline_items"))

        async for changes in awatch("./crunch/output/"):
            for a in changes:
                file_path = a[1]
                df = pd.read_csv(file_path)

                # If the predictor hasn't been instantiated yet, do it now
                if self.predictor is None and len(df.index) >= baseline_items:
                    self.predictor = CognitiveLoadPredictor(
                        df.iloc[:baseline_items, 1].values.astype(float)
                    )
                    forecast = self.predictor.current_forecast
                    is_outlier = self.predictor.is_outlier
                    # put it in the queue so the web socket can read
                    await queue.put(
                        {
                            "Current cognitive load": str(df.iloc[-1, 1].astype(float)),
                            "Forecasted cognitive load": str(forecast),
                            "Need help": str(is_outlier),
                        }
                    )

                # If the predictor has been instantiated, update and predict
                elif self.predictor:
                    new_value = df.iloc[-1, 1].astype(float)
                    self.predictor.update_and_predict(new_value)
                    forecast = self.predictor.current_forecast
                    is_outlier = self.predictor.is_outlier

                    # put it in the queue so the web socket can read
                    await queue.put(
                        {
                            "Current cognitive load": str(df.iloc[-1, 1].astype(float)),
                            "Forecasted cognitive load": str(forecast),
                            "Need help": str(is_outlier),
                        }
                    )

    async def handler(self, websocket, path, queue):
        try:
            while True:
                data = await queue.get()
                await websocket.send(json.dumps(data))
        finally:
            print("Lost connection with websocket client")

    def start_websocket(self):
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()

        local_ip = socket.gethostbyname(socket.gethostname())
        ip = (
            "127.0.0.1"
            if util.config("websocket", "use_localhost") == "True"
            else local_ip
        )
        port = int(util.config("websocket", "port"))

        print("##################################################################")
        print("###### IP: ", ip)
        print("###### Port: ", port)
        print("##################################################################")

        start_server = websockets.serve(
            functools.partial(self.handler, queue=queue), ip, port
        )
        loop.run_until_complete(
            asyncio.gather(
                start_server,
                self.watcher(queue),
            )
        )

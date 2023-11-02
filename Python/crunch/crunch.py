from multiprocessing import Process
from crunch.websocket.websocket import WebSocketServer

from crunch.empatica import start_empatica
from crunch.eyetracker import start_eyetracker


def start_processes(mobile):
    p1 = Process(target=start_empatica)
    # Uncomment line below to start Empatica
    # p1.start()

    p2 = Process(target=start_eyetracker)
    p2.start()
    websocket = WebSocketServer()

    websocket.start_websocket()

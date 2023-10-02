from multiprocessing import Process
from crunch.websocket.websocket import WebSocketServer

from crunch.empatica import start_empatica
from crunch.eyetracker import start_eyetracker
from crunch.websocket import start_websocket


def start_processes(mobile):
    p1 = Process(target=start_empatica)
    # p1.start()

    p2 = Process(target=start_eyetracker)
    p2.start()
    websocket = WebSocketServer()

    websocket.start_websocket()

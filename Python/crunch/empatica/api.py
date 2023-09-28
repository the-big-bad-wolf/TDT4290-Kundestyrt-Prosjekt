import socket
import time

import crunch.util as util
from crunch.empatica.handler import DataHandler  # noqa


class EmpaticaAPI:
    """
    EmpaticaAPI is responsible for connecting to and receiving data from the
    empatica E4 wristband, and then the API sends the data to all subscribed
    handlers. The class communicates with a streaming server to get the data
    """
    serverAddress = util.config('empatica', 'address')
    serverPort = int(util.config('empatica', 'port'))
    bufferSize = int(util.config('empatica', 'buffersize'))
    deviceID = util.config('empatica', 'deviceid')

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False

    subscribers = {"EDA": [], "IBI": [], "TEMP": [], "HR": []}

    def add_subscriber(self, data_handler, requested_data):
        """
        Adds a handler as a subscriber for a specific raw data

        :param data_handler: a data handler for a specific measurement that subscribes to a specific raw data
        :type data_handler: DataHandler
        :param requested_data: The specific raw data that the data handler subscribes to
        :type requested_data: str
        """
        assert requested_data in self.subscribers.keys()
        self.subscribers[requested_data].append(data_handler)

    def connect(self):
        """ Connect to the empatica wristband """
        self.socket.settimeout(3)
        self._connect_socket()
        self._subscribe_to_socket()
        self._stream()

    def _connect_socket(self):
        """ Create the socket connection and connect the device to the socket """
        if not self.connected:
            self.socket.connect((self.serverAddress, self.serverPort))
            self.connected = True

        self.socket.send("device_list\r\n".encode())
        response = self.socket.recv(self.bufferSize)

        if self.deviceID not in response.decode("utf-8"):
            print("Device not available, reconnecting in 10 sec...")
            time.sleep(10)
            return self.connect()

        self.socket.send(("device_connect " + self.deviceID + "\r\n").encode())
        self.socket.recv(self.bufferSize)

        self.socket.send("pause ON\r\n".encode())
        self.socket.recv(self.bufferSize)

    def _subscribe_to_socket(self):
        """ Subscribe to the data on the socket connection """
        self.socket.send(("device_subscribe " + 'gsr' + " ON\r\n").encode())
        self.socket.recv(self.bufferSize)

        self.socket.send(("device_subscribe " + 'tmp' + " ON\r\n").encode())
        self.socket.recv(self.bufferSize)

        self.socket.send(("device_subscribe " + 'ibi' + " ON\r\n").encode())
        self.socket.recv(self.bufferSize)

        """
        UNUSED DATA POINTS
        self.socket.send(("device_subscribe " + 'bvp' + " ON\r\n").encode())
        self.socket.recv(self.bufferSize)

        self.socket.send(("device_subscribe " + 'acc' + " ON\r\n").encode())
        self.socket.recv(self.bufferSize)
        """

        self.socket.send("pause OFF\r\n".encode())
        self.socket.recv(self.bufferSize)

    def _stream(self):
        """ Continuously receive data from the socket connection """
        while True:
            try:
                response = self.socket.recv(self.bufferSize).decode("utf-8")
                if "connection lost to device" in response:
                    print("Lost connection to device, reconnecting in 10 sec...")
                    time.sleep(10)
                    return self.connect()
                if "turned off via button" in response:
                    print("The wristband was turned off, reconnecting in 10 sec...")
                    time.sleep(10)
                    return self.connect()

                samples = response.split("\n")
                for i in range(len(samples) - 1):
                    name = samples[i].split()[0]
                    data = float(samples[i].split()[2].replace(',', '.'))
                    if name == "E4_Temperature":
                        self._send_data_to_subscriber("TEMP", data)
                    elif name == "E4_Gsr":
                        self._send_data_to_subscriber("EDA", data)
                    elif name == "E4_Hr":
                        self._send_data_to_subscriber("HR", data)
                    elif name == "E4_Ibi":
                        self._send_data_to_subscriber("IBI", data)

                    """
                    UNUSED DATA POINTS
                    if name == "E4_Bvp":
                        self.send_data_to_subscriber("BVP", data)
                    if name == "E4_Acc":
                        self.send_data_to_subscriber("ACC", data)
                    """

            except socket.timeout:
                print("Socket timeout, reconnecting in 10 sec...")
                time.sleep(10)
                return self.connect()

    def _send_data_to_subscriber(self, name, data):
        """
        Sends the specified data to all handlers that are subscribing to it

        :param name: The name of the data point we are sending
        :type name: str
        :param data: The datapoint we are sending
        :type data: float
        """
        for handler in self.subscribers[name]:
            handler.add_data_point(data)

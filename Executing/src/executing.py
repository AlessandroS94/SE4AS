import threading
import time
from datetime import datetime
import pandas as pd
import logging
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")


class Service(threading.Thread):
    def __init__(self, host, port, topicExecuting):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.topicExecuting = topicExecuting
        self.client_id = f'python-mqtt-{10}'
        self.payload = []

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.host, self.port)
        return client

    def subscribe(self, client: mqtt_client):

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            logging.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            if msg.topic == "/channel/BLANKET-executing":
                with open("./executing.csv", 'a+') as f:
                    f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")

        client.subscribe(self.topicExecuting)
        client.on_message = on_message

    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()


class Executing(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(f'python-mqtt-{9}')

        client.on_connect = on_connect
        client.connect(service.host, service.port)
        return client

    def publish(self, client):
        while True:
            try:
                data = pd.read_csv("./executing.csv")
                data = pd.DataFrame(data, columns=['Date', 'BLANKET'])
                blanket = data['BLANKET'][(len(data)) - 1]
                result = client.publish("/channel/BLANKET-sensor", str(blanket))
                status = result[0]
                if status == 0:
                    print("Set blanket value:\n", blanket)
                    logging.info(f"Set blanket value: {blanket}")
                else:
                    logging.info(f"Failed to send message to topic /executing/BLANKET:  {blanket}")

                time.sleep(2)
            except Exception as e :
                print('erorr' + e)
                logging.info(f"It has occurred this error:: {e}")



    def run(self):
        client = self.connect_mqtt()
        self.publish(client)


service = Service('127.0.0.1', 1883, "/channel/BLANKET-executing")
service.start()
time.sleep(4)
executing = Executing()
executing.start()

import threading
import time
from datetime import datetime
import pandas as pd
import logging
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")


class Service(threading.Thread):
    def __init__(self, host, port, topicHr, topicTemperature, topicPrevisiong):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.topicHR = topicHr
        self.topicTEMP = topicTemperature
        self.topicPrevisioning = topicPrevisiong
        self.client_id = f'python-mqtt-{8}'
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
            if msg.topic == "/channel/HR-sensor":
                with open("./HR-sensor.csv", 'a+') as f:
                    f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")
            if msg.topic == "/channel/TEMP-sensor":
                with open("./TEMP-sensor.csv", 'a+') as f:
                    f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")
            if msg.topic == "/channel/BLANKET-prediction":
                with open("./BLANKET-prediction.csv", 'a+') as f:
                    f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")


        client.subscribe(self.topicHR)
        client.on_message = on_message

        client.subscribe(self.topicTEMP)
        client.on_message = on_message

        client.subscribe(self.topicPrevisioning)
        client.on_message = on_message

    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()


class Planning(threading.Thread):

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
            dataHR = pd.read_csv("./HR-sensor.csv")
            dataTEMP = pd.read_csv("./TEMP-sensor.csv")
            dataPREVISIONING = pd.read_csv("./BLANKET-prediction.csv")
            dataHR = pd.DataFrame(dataHR, columns=['Date', 'HR'])
            dataTEMP = pd.DataFrame(dataTEMP, columns=['Date', 'TEMP'])
            dataPREVISIONING = pd.DataFrame(dataPREVISIONING, columns=['Date', 'PREDICT'])

            if int(dataTEMP['TEMP'][(len(dataTEMP)) - 1]) < int(41):
                 blanket = dataPREVISIONING['PREDICT'][(len(dataPREVISIONING)) - 1]
            else:
                 blanket = int(0)
            result = client.publish("/channel/BLANKET-executing", str(blanket))
            status = result[0]
            if status == 0:
                print("Set blanket value:\n", blanket)
                logging.info(f"Set blanket value: {blanket}")
            else:
                logging.info(f"Failed to send message to topic /executing/BLANKET:  {blanket}")
            time.sleep(4)

    def run(self):
        client = self.connect_mqtt()
        self.publish(client)


service = Service('127.0.0.1', 1883, "/channel/HR-sensor", "/channel/TEMP-sensor", "/channel/BLANKET-prediction")
service.start()
time.sleep(4)
plan = Planning()
plan.start()

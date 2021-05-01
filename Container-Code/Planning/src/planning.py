import os
import threading
import time
from datetime import datetime
import pandas as pd
import logging
import yaml
from flask import Flask
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

app = Flask(__name__)


@app.route('/isAlive')
def index():
    return "true"

class Service(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.topicTEMPERATURElimit = "/channel/TEMPERATURE-limit"
        self.topicTEMP = "/channel/TEMP-sensor"
        self.topicPrevisioning = "/channel/BLANKET-prediction"
        self.client_id = f'python-mqtt-{5}'
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
            try:
                if msg.topic == "/channel/TEMPERATURE-limit":
                    with open("./TEMPERATURE-limit.csv", 'a+') as f:
                        f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")
                if msg.topic == "/channel/TEMP-sensor":
                    with open("./TEMP-sensor.csv", 'a+') as f:
                        f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")
                if msg.topic == "/channel/BLANKET-prediction":
                    with open("./BLANKET-prediction.csv", 'a+') as f:
                        f.write("" + datetime.now().timestamp().__int__().__str__() + "," + msg.payload.decode() + "\n")
            except Exception as excM:
                logging.info(
                    f"Exeption: {excM} -- {time.asctime(time.localtime(time.time()))}")
                pidP = os.getpid()
                os.kill(pidP, 2)

        client.subscribe(self.topicTEMPERATURElimit)
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

    def __init__(self, service, MINTEMPERATUREBLANKET):
        threading.Thread.__init__(self)
        self.service = service
        self.MINTEMPERATUREBLANKET = MINTEMPERATUREBLANKET

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        try:
            client = mqtt_client.Client(f'python-mqtt-{6}')
            client.on_connect = on_connect
            client.connect(self.service.host, self.service.port)
            return client
        except Exception as excM:
            logging.info(f"Execption: {excM} -- {time.asctime(time.localtime(time.time()))}")
            pidP = os.getpid()
            os.kill(pidP, 2)

    def publish(self, client):
        while True:
            try:
                time.sleep(18)
                dataTEMPLimit = pd.read_csv("./TEMPERATURE-limit.csv")
                dataTEMP = pd.read_csv("./TEMP-sensor.csv")
                dataPREVISIONING = pd.read_csv("./BLANKET-prediction.csv")
                dataTEMPLimit = pd.DataFrame(dataTEMPLimit, columns=['Date', 'TEMPERATURELIMIT'])
                dataTEMP = pd.DataFrame(dataTEMP, columns=['Date', 'TEMP'])
                dataPREVISIONING = pd.DataFrame(dataPREVISIONING, columns=['Date', 'PREDICT'])

                if int(dataTEMP['TEMP'][(len(dataTEMP)) - 1]) < int(
                        dataTEMPLimit['TEMPERATURELIMIT'][(len(dataTEMPLimit)) - 1]):
                    blanket = dataPREVISIONING['PREDICT'][(len(dataPREVISIONING)) - 1]
                else:
                    blanket = self.MINTEMPERATUREBLANKET
                result = client.publish("/channel/BLANKET-executing", str(blanket))
                status = result[0]
                if status == 0:
                    print("Set blanket value:\n", blanket)
                    logging.info(f"Set blanket value: {blanket} -- {time.asctime(time.localtime(time.time()))}")
                else:
                    logging.info(
                        f"Failed to send message to topic /executing/BLANKET:  {blanket} -- {time.asctime(time.localtime(time.time()))}")
            except Exception as exceptionM:
                logging.info(
                    f"Exeptionc {exceptionM} -- {time.asctime(time.localtime(time.time()))}")
                pidP = os.getpid()
                os.kill(pidP, 2)

            time.sleep(4)

    def run(self):
        client = self.connect_mqtt()
        self.publish(client)


def main ():
    with open("settings.yaml", 'r') as stream:
        try:
            settings = yaml.safe_load(stream)
            MOSQUITTODNS = settings['mosquittoDNS']
            MOSQUITTOPORT = settings['mosquittoPORT']
            MINTEMPERATUREBLANKET = settings['MINTEMPERATUREBLANKET']
        except yaml.YAMLError as exc:
            logging.info(f"Failed to reading settings-- {time.asctime(time.localtime(time.time()))}")
            pidP = os.getpid()
            os.kill(pidP, 2)
    service = Service(MOSQUITTODNS, MOSQUITTOPORT)
    service.start()
    time.sleep(4)
    plan = Planning(service, MINTEMPERATUREBLANKET)
    plan.start()

    #app.run(host="0.0.0.0", port="8082")


if __name__ == '__main__':
    main()

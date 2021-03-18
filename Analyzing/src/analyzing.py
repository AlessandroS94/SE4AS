import threading
import pandas as pd
import numpy as np
import time
from datetime import datetime
from sklearn.linear_model import LinearRegression
import logging
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")


class Service(threading.Thread):
    def __init__(self, host, port, topicHr, topicTemperature, topicBlanket, topicPrevisiong):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.topicHR = topicHr
        self.topicTEMP = topicTemperature
        self.topicBLANKET = topicBlanket
        self.topicPrevisioning = topicPrevisiong
        self.dataset = './health.csv'
        self.client_id = f'python-mqtt-{2}'
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
            if msg.topic == "/sensor/HR":
                with open(self.dataset, 'a+') as f:
                    f.write("" + datetime.now().timestamp().__int__().__str__())
                with open('./health.csv', 'a+') as f:
                    f.write("," + msg.payload.decode())
            if msg.topic ==  "/sensor/TEMP":
                with open('./health.csv', 'a+') as f:
                    f.write("," + msg.payload.decode())
            if msg.topic == "/sensor/BLANKET":
                with open('./health.csv', 'a+') as f:
                    f.write("," + msg.payload.decode())
                with open(self.dataset, 'a+') as f:
                    f.write("\n")


        client.subscribe(self.topicHR)
        client.on_message = on_message

        client.subscribe(self.topicTEMP)
        client.on_message = on_message

        client.subscribe(self.topicBLANKET)
        client.on_message = on_message


    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()


class ML(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(f'python-mqtt-{3}')

        client.on_connect = on_connect
        client.connect(service.host, service.port)
        return client

    def publish(self,client):
        while True:
            data = pd.read_csv(service.dataset)
            data = pd.DataFrame(data, columns=['Date', 'BLANKET'])
            X = np.array(data)[:, 0].reshape(-1, 1)
            y = np.array(data)[:, 1].reshape(-1, 1)
            to_predict_x = [data['Date'][len(data['Date']) - 1] + 1]
            to_predict_x = np.array(to_predict_x).reshape(-1, 1)
            regsr = LinearRegression()
            regsr.fit(X, y)
            predicted_y = regsr.predict(to_predict_x)
            result = client.publish("/prediction/BLANKET", str(predicted_y.__int__()))
            status = result[0]
            if status == 0:
                print("Predicted blanket value:\n", predicted_y.__int__())
                logging.info(f"Predicted blanket value: {predicted_y.__int__()}")
            else:
                logging.info(f"Failed to send message to topic {predicted_y.__int__()}")
            time.sleep(2)

    def run(self):
        client = self.connect_mqtt()
        self.publish(client)



service = Service('127.0.0.1', 1883, "/sensor/HR", "/sensor/TEMP", "/sensor/BLANKET", "/prediction/BLANKET")
service.start()
ml = ML()
ml.start()



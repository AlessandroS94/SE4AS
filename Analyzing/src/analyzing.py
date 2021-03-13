import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import logging
from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

dataset = pd.read_csv('./health.csv')
data = pd.DataFrame(dataset, columns=['Date', 'BLANKET'])
X = np.array(data)[:, 0].reshape(-1, 1)
y = np.array(data)[:, 1].reshape(-1, 1)
to_predict_x = [data['Date'][len(data['Date']) - 1] + 1]
to_predict_x = np.array(to_predict_x).reshape(-1, 1)

regsr = LinearRegression()
regsr.fit(X, y)

predicted_y = regsr.predict(to_predict_x)

print("Predicted blanket value:\n", predicted_y.__int__())


class Ml:
    def __init__(self, host,port, topicHr, topicTemperature, topicBlanket):
        self.host = host
        self.port = port
        self.topicHR = topicHr
        self.topicTEMP = topicTemperature
        self.topicBLANKET = topicBlanket
        self.dataset = pd.read_csv('./health.csv')
        self.client_id = f'python-mqtt-{2}'

    def info(self):
        adding = {'Date': datetime.now().timestamp().__int__(), 'HR': 99, 'TEMPERATURE': 40, 'BLANKET': 87}
        self.dataset = self.dataset.append(adding, ignore_index=True)
        print(self.dataset)
        print('host'+ self.host + '\n' +  'port:' + str(self.port))

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

        client.subscribe(self.topicHR)
        client.on_message = on_message

        client.subscribe(self.topicBLANKET)
        client.on_message = on_message

        client.subscribe(self.topicTEMP)
        client.on_message = on_message

    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()



ml = Ml('127.0.0.1', 1883, "/sensor/HR", "/sensor/TEMP", "/sensor/BLANKET")
ml.info()
ml.run()

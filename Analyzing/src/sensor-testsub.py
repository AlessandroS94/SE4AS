import random
import logging

from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")


broker = '127.0.0.1'
port = 1883
topicHR = "/sensor/HR"
topicTEMP = "/sensor/TEMP"
topicBLANKET = "/sensor/BLANKET"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{2}'



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        logging.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topicHR)
    client.on_message = on_message

    client.subscribe(topicBLANKET)
    client.on_message = on_message

    client.subscribe(topicTEMP)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
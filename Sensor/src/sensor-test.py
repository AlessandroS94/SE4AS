import random
import time
import logging

from paho.mqtt import client as mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

broker = '127.0.0.1'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{1}'
topicHR = "/sensor/HR"
topicTEMP = "/sensor/TEMP"
topicBLANKET = "/sensor/BLANKET"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(3)
        msgHR = random.randint(10,180)
        result = client.publish(topicHR, msgHR)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{msgHR}` to topic `{topicHR}`")
        else:
            logging.info(f"Failed to send message to topic {topicHR}")
        msgTEMP = random.randint(33, 43)
        result = client.publish(topicTEMP, msgTEMP)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{msgTEMP}` to topic `{topicTEMP}`")
        else:
            logging.info(f"Failed to send message to topic {topicTEMP}")
        msgBLANKET = random.randint(0, 80)
        result = client.publish(topicBLANKET, msgBLANKET)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{msgBLANKET}` to topic `{topicBLANKET}`")
        else:
            logging.info(f"Failed to send message to topic {topicBLANKET}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
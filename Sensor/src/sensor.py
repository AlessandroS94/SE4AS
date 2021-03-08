import logging
import random
import time
import sys



import paho.mqtt.client as mqtt #import the client1

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
broker_address="127.0.0.1:11883"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF")
time.sleep(4) # wait
client.loop_stop() #stop the loop

while True:
    print("SENSOR HR")
    n = random.randint(50, 180)
    print(n)
    logging.info("SENSOR HR " + str(n))

    print("SENSOR TEMPERATURE")
    n = random.randint(35, 43)
    print(n)
    logging.info("SENSOR TEMPERATURE " + str(n))

    print("SENSOR BLANKET")
    n = random.randint(0, 60)
    print(n)
    logging.info("SENSOR BLANKET " + str(n))

    old_stdout = sys.stdout

    log_file = open("message.log", "w")

    sys.stdout = log_file

    print
    "this will be written to message.log"

    sys.stdout = old_stdout

    log_file.close()
    time.sleep(5)

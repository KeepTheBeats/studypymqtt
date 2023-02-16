"""
    Code for measuring MQTT PACKET LOSS IN NODE1
"""

#Libraries
from paho.mqtt import client as mqtt_client
import time
import datetime
from datetime import datetime
from threading import Thread
import csv
import logging

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger()

#Broker Address
broker_address = "192.168.100.161"
# broker_address = "172.26.24.61"
#broker_address = "broker.emqx.io"
#Broker port
broker_port = 1883
#Publishing topic
# topic_pub = "request"
topic_pub = "test/test1/test11"
#QoS level
qos_level = 2

#MQTT credentials
username = "testbed"
passwd = "1234"


#Function for connecting the broker
def connect_mqtt() -> mqtt_client:

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            _logger.warning("Connected to MQTT Broker!\n")
        else:
            _logger.warning("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    # client.username_pw_set(username, passwd)
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)
    return client


#PUBLISH function
def publish(client: mqtt_client.Client):
    global sent_time, qos_level
    #We sent from 0 to 99
    for i in range(0, 100):
        tx_msg = str(i)
        #We publish the message
        result = client.publish(topic_pub, tx_msg, qos=qos_level)

        #State code
        status = result[0]
        if status == 0:
            _logger.warning("Published message: " + tx_msg)
            _logger.warning("Topic: " + topic_pub)
        else:
            _logger.warning(f"Failed to send message to topic {topic_pub}")

        time.sleep(0.25)


#Main function
def run():

    #We connect
    client = connect_mqtt()
    client.loop_start()
    publish(client)

    #We sleep 5 seconds because we should wait for all the packets to be finished
    time.sleep(5)
    client.loop_stop()
    client.disconnect()


#=========================== MQTT ======================================

if __name__ == '__main__':
    run()

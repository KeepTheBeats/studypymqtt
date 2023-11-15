"""
    Code for measuring MQTT PACKET LOSS IN NODE 2
"""

#Libraries
from paho.mqtt import client as mqtt_client
from threading import Thread
import time
import logging

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger()

#Broker address
broker_address = "192.168.100.161"
# broker_address = "172.26.24.61"
#broker_address = "broker.emqx.io"
#Broker port
broker_port = 1883
#Subscribing topic
# topic_sub = "request"
topic_sub = "test/test1/test11"
#QoS level
qos_level = 2
#Number of lost packets
count_lost = 0
#Number of repeated packets
count_repeat = 0

#Diccionary for storing the packets and study them
packet_dict = {}
for i in range(0, 100):
    packet_dict[i] = 0

#MQTT credentials
username = "testbed"
passwd = "1234"


#Function for connecting the broker
def connect_mqtt() -> mqtt_client.Client:

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            _logger.warning("Connected to MQTT Broker!\n")
        else:
            _logger.warning("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    # client.username_pw_set(username, passwd)
    client.on_connect = on_connect
    client.connect(broker_address, broker_port, keepalive=60)
    return client


#SUBSCRIBE function
def subscribe(client: mqtt_client.Client):
    global qos_level

    def on_message(client, userdata, msg):
        #What we receive
        index_rx_msg = msg.payload.decode()
        _logger.warning("Received: " + index_rx_msg)
        #We add as the index of dict the package. The value of that key, we sum +1 so if it is retransmitted, we will know. If it never arrives it will be 0
        packet_dict[int(index_rx_msg)] = packet_dict[int(index_rx_msg)] + 1
        _logger.warning("Received: " + index_rx_msg + "Finished")

    client.subscribe(topic_sub, qos=qos_level)
    _logger.warning("Subscribed to topic: " + topic_sub)
    client.on_message = on_message


#Function for
def handle_data():
    global count_lost, count_repeat
    time.sleep(35)
    for i in range(0, 100):
        if packet_dict[i] > 1:
            _logger.warning("PACKET {} IS REPEATED".format(i))
            _logger.warning("COUNT: {}".format(packet_dict[i]))
            count_repeat = count_repeat + 1

    for i in range(0, 100):
        if packet_dict[i] == 0:
            _logger.warning("PACKET {} IS LOST".format(i))
            _logger.warning("COUNT: {}".format(packet_dict[i]))
            count_lost = count_lost + 1
    _logger.warning("FINISHED!")
    _logger.warning("LOST PACKETS: {}".format(count_lost))
    _logger.warning("REPEATED PACKETS: {}".format(count_repeat))


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    thread_sub = Thread(target=handle_data)
    thread_sub.start()
    run()

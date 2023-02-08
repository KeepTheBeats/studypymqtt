import datetime
import time
import rfc3339
import pytz
from paho.mqtt import client as mqtt_client

broker_ip = "192.168.100.161"
broker_port = 1883
topic = "test/test1/test11"


def connect_mqtt() -> mqtt_client.Client:

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connect to broker successful!")
        else:
            print("Connect to broker failed, return code: %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker_ip, broker_port)
    return client


def subscribe(client: mqtt_client.Client):

    def on_message(client, userdata, msg):
        print("Receive [{}] from topic {}".format(msg.payload.decode(),
                                                  msg.topic))

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()

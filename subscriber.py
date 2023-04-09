import datetime
import time
import rfc3339
import pytz
import logging
from paho.mqtt import client as mqtt_client

broker_ip = "192.168.100.161"
# broker_ip = "172.26.24.61"
broker_port = 1883
topic = "test/test1/test11"

broker_user = "testbed"
broker_passwd = "1234"

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger()


def connect_mqtt() -> mqtt_client.Client:

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            _logger.warning("Connect to broker successful!")
        else:
            _logger.warning("Connect to broker failed, return code: %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker_ip, broker_port)
    # client.username_pw_set(broker_user, broker_passwd)
    return client


def subscribe(client: mqtt_client.Client):

    def on_message(client, userdata, msg):
        infomation = msg.payload.decode().split("|")[0]
        _logger.warning("Receive [{}] from topic {}".format(
            infomation, msg.topic))

    client.subscribe(topic, qos=2)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == "__main__":
    run()

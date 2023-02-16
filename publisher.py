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


def connect_mqtt():

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


def publish(client: mqtt_client.Client):
    msg_count = 0
    while True:
        time_msg = datetime.datetime.now(tz=pytz.timezone("CET"))
        time_msg_str = rfc3339.format_microsecond(time_msg,
                                                  utc=False,
                                                  use_system_timezone=False)
        msg = f"No. {msg_count}, time: {time_msg_str}"
        res = client.publish(topic, msg, qos=2)
        status = res[0]
        if status == 0:
            _logger.warning("send {} to topic {} successfully".format(
                msg, topic))
        else:
            _logger.warning("send {} to topic {} fail".format(msg, topic))
        msg_count += 1
        time.sleep(0.25)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    run()

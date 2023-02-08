# studypymqtt
study Python MQTT following the guidance in `https://www.emqx.com/en/blog/how-to-use-mqtt-in-python`

Before running the publisher and subcriber, a broker is deployed on 192.169.100.161:1883 by the command: `docker run -d --restart=always --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx`
import paho.mqtt.client as mqtt
import datetime
import json
import random
import time


class ServerCom:
    SENSORS = 'sensors'

    def __init__(self, server_port=1883, server_host='ec2-18-185-135-181.eu-central-1.compute.amazonaws.com'):
        self.server_port = server_port
        self.server_host = server_host
        self.mqtt_c = mqtt.Client("gateway")
        self.connect()

    def connect(self):
        def on_connect(mqttc, obj, flags, rc):
            self.mqtt_c.subscribe(self.SENSORS, qos=2)
            print('Connected')

        def on_publish(mqttc, obj, mid):
            print("published", mid)
            pass

        def on_message(client, userdata, msg):
            print('msg: ', msg)
            msg_data = json.loads(msg.payload.decode('utf-8'))
            print('msg_data: ', msg_data)
            msg_data['timestamp'] = datetime.datetime.fromtimestamp(int(msg_data['timestamp']) / 1e3)
            print(msg_data)

        self.mqtt_c.on_connect = on_connect
        self.mqtt_c.on_publish = on_publish
        self.mqtt_c.connect(self.server_host, self.server_port, 45)
        self.mqtt_c.on_message = on_message
        self.mqtt_c.loop_start()

    def publish_temperature(self, temperature):
        ret = self.mqtt_c.publish(self.SENSORS, str(temperature), qos=2)
        ret.wait_for_publish()


if __name__ == "__main__":
    com = ServerCom()

    msg = '{"sensor": "moisture", "data": "' + str(random.randint(1, 101)) + '"}'
    com.publish_temperature(msg)
    msg = '{"sensor": "moisture", "data": "' + str(random.randint(1, 101)) + '"}'
    com.publish_temperature(msg)
    msg = '{"sensor": "moisture", "data": "' + str(random.randint(1, 101)) + '"}'
    com.publish_temperature(msg)
    x = input()

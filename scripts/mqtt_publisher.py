import paho.mqtt.client as mqtt
import json
import time
import os


# import random


class Publisher:

    def __init__(self, topic, sensor_type, server_port=1883, server_host='localhost'):

        if 'SERVER_PORT' in os.environ:
            self.server_port = os.environ['SERVER_PORT']
        else:
            self.server_port = server_port
        if 'SERVER_HOST' in os.environ:
            self.server_host = os.environ['SERVER_HOST']
        else:
            self.server_host = server_host
        self.topic = topic

        print("Connect to", self.server_host, self.server_port, " with topic ", self.topic)

        self.mqtt_c = mqtt.Client(os.environ['DEVICE_NAME'] + '_' + sensor_type)
        self.connect()

    def connect(self):
        def on_connect(mqttc, obj, flags, rc):
            print('Connected')

        def on_publish(mqttc, obj, mid):
            print("published to: ", self.topic)
            pass

        self.mqtt_c.on_connect = on_connect
        self.mqtt_c.on_publish = on_publish
        self.mqtt_c.connect(self.server_host, self.server_port, 45)
        self.mqtt_c.loop_start()

    def publish_sensor_data(self, sensor, value):
        msg = '{"device_id": "' + os.environ['DEVICE_NAME'] + '", "measurement": "' + sensor + '", "data": ' + str(
            value) + ', "timestamp": ' + str(int(time.time())) + '}'
        print(msg)
        ret = self.mqtt_c.publish(self.topic, msg, qos=2)
        ret.wait_for_publish()

# if __name__ == "__main__":
# com = ServerCom(server_host='3.122.180.139')

# com.publish_sensor_data('water_level', str(random.randint(1, 101)))
# time.sleep(1)

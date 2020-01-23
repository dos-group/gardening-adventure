import paho.mqtt.client as mqtt
import json
import time
import getpass
import os
import random


class ServerCom:
    SENSORS = 'sensors'

    def __init__(self, server_port=1883, server_host='localhost'):

        if 'SERVER_PORT' in os.environ:
            self.server_port = os.environ['SERVER_PORT']
        else:
            self.server_port = server_port
        if 'SERVER_HOST' in os.environ:
            self.server_host = os.environ['SERVER_HOST']
        else:
            self.server_host = server_host

        self.mqtt_c = mqtt.Client("gateway")
        self.connect()
        # self.mqtt_c.loop_forever()

    def connect(self):
        def on_connect(mqttc, obj, flags, rc):
            self.mqtt_c.subscribe(self.SENSORS, qos=2)
            print('Connected')

        def on_publish(mqttc, obj, mid):
            print("published", mqttc, obj, mid)
            pass

        def on_message(client, userdata, msg):
            print('msg: ', msg)
            msg_data = json.loads(msg.payload.decode('utf-8'))
            print('msg_data: ', msg_data)

        self.mqtt_c.on_connect = on_connect
        self.mqtt_c.on_publish = on_publish
        self.mqtt_c.connect(self.server_host, self.server_port, 45)
        self.mqtt_c.on_message = on_message
        self.mqtt_c.loop_start()

    def publish_sensor_data(self, sensor, value):
        device_id = getpass.getuser()
        msg = '{"device_id": "' + device_id + '", "measurement": "' + sensor + '", "data": ' + str(
            value) + ', "timestamp": ' + str(int(time.time())) + '}'
        print(msg)
        ret = self.mqtt_c.publish(self.SENSORS, msg, qos=2)
        ret.wait_for_publish()

# if __name__ == "__main__":
# com = ServerCom(server_host='3.122.180.139')

# com.publish_sensor_data('water_level', str(random.randint(1, 101)))
# time.sleep(1)

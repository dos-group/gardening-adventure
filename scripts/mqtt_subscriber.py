import paho.mqtt.client as mqtt
import json
import getpass
import os


# import random


class Subscriber:

    def __init__(self, topic, callback, server_port=1883, server_host='localhost'):

        if 'SERVER_PORT' in os.environ:
            self.server_port = os.environ['SERVER_PORT']
        else:
            self.server_port = server_port
        if 'SERVER_HOST' in os.environ:
            self.server_host = os.environ['SERVER_HOST']
        else:
            self.server_host = server_host
        self.topic = topic
        self.callback = callback
        print("Connect to", self.server_host, self.server_port, ' with topic ', self.topic)

        self.mqtt_c = mqtt.Client(getpass.getuser())
        self.connect()
        self.mqtt_c.loop_forever()

    def connect(self):
        def on_connect(mqttc, userdata, flags, rc):
            if rc == 0:
                print('successful connection ','subscribe topic: ', self.topic )
                self.mqtt_c.subscribe(self.topic, qos=2)
            else:
                print('connection fail')

        def on_message(client, userdata, msg):
            msg_data = json.loads(msg.payload.decode('utf-8'))
            print('msg_data: ', msg_data)
            self.callback(msg_data)

        self.mqtt_c.on_connect = on_connect
        self.mqtt_c.connect(self.server_host, self.server_port, 45)
        self.mqtt_c.on_message = on_message
        self.mqtt_c.loop_start()

import paho.mqtt.client as mqtt
import datetime
import json


class ServerCom:

    SENSORS = 'sensors'
    THRESHOLD_CH = 'threshold/change'
    TERMINAL = 'terminal'
    CONNECTED = 'connected'

    def __init__(self, terminal, server_port=1883, server_host='ec2-18-185-135-181.eu-central-1.compute.amazonaws.com'):
        self.terminal = terminal
        self.server_port = server_port
        self.server_host = server_host
        self.mqtt_c = mqtt.Client(self.TERMINAL)
        self.connect()

    def connect(self):
        def on_connect(mqttc, obj, flags, rc):
            self.mqtt_c.subscribe(self.SENSORS, qos=2)
            print('Connected')

        def on_publish(mqttc, obj, mid):
            pass

        def on_message(client, userdata, msg):
            msg_data = json.loads(msg.payload.decode('utf-8'))
            msg_data['timestamp'] = datetime.datetime.fromtimestamp(int(msg_data['timestamp']) / 1e3)
            self.terminal.set_threshold(msg_data)

        self.mqtt_c.on_connect = on_connect
        self.mqtt_c.on_publish = on_publish
        self.mqtt_c.connect(self.server_host, self.server_port, 60)
        self.mqtt_c.on_message = on_message
        self.mqtt_c.loop_start()

    def publish_temperature(self, temperature):
        ret = self.mqtt_c.publish(self.TEMPERATURE, str(temperature), qos=2)
        ret.wait_for_publish()

    def publish_on_status(self, on):
        now = datetime.datetime.now()

        on_message = '{\"timestamp\": \"' + str(now.isoformat()) + '\", \"on\": \"' + str(on) + '\"}'
        ret = self.mqtt_c.publish(self.ON, on_message, qos=2)

        ret.wait_for_publish()

    def publish_threshold(self, threshold):
        now = datetime.datetime.now()
        threshold_message = '{\"timestamp\": \"' + str(now.isoformat()) + '\", \"threshold\": \"' + str(
            threshold) + '\"}'
        ret = self.mqtt_c.publish(self.THRESHOLD_VA, str(threshold_message), qos=2)
        ret.wait_for_publish()

    def publish_connected(self):
        now = int(int(datetime.datetime.now().strftime("%s%f")) / 1000)
        ret = self.mqtt_c.publish(self.CONNECTED, str(now))
        ret.wait_for_publish()


import Adafruit_DHT as dht
from time import sleep
from mqtt_publisher import Publisher
import os


class DHT:
    DELAY_INTERVAL = 2
    TOPIC = 'sensor/dht/'

    def __init__(self):
        self.mqtt_client = Publisher(self.TOPIC + os.environ['DEVICE_NAME'], 'dht')
        self.collector()

    def read(self):
        h, t = dht.read_retry(dht.DHT22, 4)
        if h is not None and t is not None:
            return '{0:0.1f}*C'.format(t), '{0:0.1f}%'.format(h)
        else:
            print('failed to retrieve the data')

    def collector(self):
        print('start collecting air sensor data')
        while True:
            temp_value, hum_value = self.read()
            self.mqtt_client.publish_sensor_data("dht_temp", temp_value)
            self.mqtt_client.publish_sensor_data("dht_hum", hum_value)
            sleep(DHT.DELAY_INTERVAL)


if __name__ == '__main__':
    dht = DHT()

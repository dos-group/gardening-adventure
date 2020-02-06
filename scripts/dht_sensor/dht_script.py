import Adafruit_DHT as dht
from time import sleep
from mqtt_client import ServerCom


class DHT:
    DELAY_INTERVAL = 2

    def __init__(self):
        self.mqtt_client = ServerCom()

    def read(self):
        h, t = dht.read_retry(dht.DHT22, 4)
        if h is not None and t is not None:
            return '{0:0.1f}*C'.format(t), '{1:0.1f}%'.format(h)
        else:
            print('failed to retrieve the data')

    def collector(self):
        print('start collecting air sensor data')
        while True:
            temp_value, hum_value = self.read()
            print('Temperature at: ', temp_value, ' Humidity at: ', hum_value)
            self.mqtt_client.publish_sensor_data("dht_temp", temp_value)
            self.mqtt_client.publish_sensor_data("dht_hum", hum_value)
            sleep(DHT.DELAY_INTERVAL)

import Adafruit_DHT as dht
from time import sleep
from mqtt_client import ServerCom

DELAY_INTERVAL = 5
client = ServerCom()

while True:
	h,t = dht.read_retry(dht.DHT22, 4)
	if h is not None and t is not None:
		print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h))
		client.mqtt_client.publish_sensor_data("temp", '{0:0.1f}*C'.format(t))
		client.mqtt_client.publish_sensor_data("humidity", '{1:0.1f}%'.format(h))
	else:
		print('failed to retrieve the data')
	sleep(DELAY_INTERVAL)

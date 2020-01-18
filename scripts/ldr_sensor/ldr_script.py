from gpiozero import LightSensor
from time import sleep
from mqtt_client import ServerCom

DELAY_INTERVAL = 5

ldr = LightSensor(25)
client = ServerCom()

while True:
	print(ldr.value)
	client.publish_sensor_data("luminance", ldr.value)
	sleep(DELAY_INTERVAL)



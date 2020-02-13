import spidev
import ws2812

from mqtt_subscriber import Subscriber


class RGB_Light:
    LIGHT_TOPIC = "actor/rgb_light/"

    def __init__(self, light_id, num_led=12):
        self.num_led = num_led
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.mqtt_client = Subscriber(self.LIGHT_TOPIC + str(light_id), self.callback)

    def callback(self, msg):
        print(msg['data'])
        if len(msg['data']) == self.num_led:
            ws2812.write2812(self.spi, msg['data'])


# cyan
# ws2812.write2812(spi, [[10,0,100]])
# off
# ws2812.write2812(spi, [[0,0,0]])
# green
# ws2812.write2812(spi, [[10,0,0]])
# very bright green

if __name__ == "__main__":
    li = RGB_Light(1)
#    com = Subscriber('actor/rgb_light/1', RGB_Light.callback, server_host='broker.hivemq.com', server_port=1883)

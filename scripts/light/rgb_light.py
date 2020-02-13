import spidev
import ws2812
import getpass
import board
import neopixel

from mqtt_subscriber import Subscriber


class LightRGB:
    LIGHT_TOPIC = "sensor/light/"

    def __init__(self, num_led=12):
        self.num_led = num_led
        self.pixels = neopixel.NeoPixel(board.D18, self.num_led)
        self.mqtt_client = Subscriber(self.LIGHT_TOPIC + getpass.getuser(), self.callback)

    def callback(self, msg):
        print(msg['data'])
        if msg['data'] > 1000:
            brightness = 255
        else:
            brightness = int(msg['data'] * 0.255)

        self.pixels[0:] = [[brightness, brightness, brightness] for i in range(self.num_led)]


if __name__ == "__main__":
    li = LightRGB()
#    com = Subscriber('actor/rgb_light/1', RGB_Light.callback, server_host='broker.hivemq.com', server_port=1883)

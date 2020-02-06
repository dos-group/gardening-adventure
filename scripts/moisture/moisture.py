from time import sleep
import RPi.GPIO as GPIO

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_MCP3008


class Moisture():
    # Software SPI configuration:
    CLK = 11
    MISO = 9
    MOSI = 10
    CS = 8
    DELAY_INTERVAL = 2

    def __init__(self):
        # Setup the GPIO board
        GPIO.setmode(GPIO.BCM)

        # Setup the switch pin
        # SWITCH = 20
        # GPIO.setup(SWITCH, GPIO.OUT)

        self.mcp = Adafruit_MCP3008.MCP3008(clk=Moisture.CLK, cs=Moisture.CS, miso=Moisture.MISO, mosi=Moisture.MOSI)

    def read(self):
        #        GPIO.output(SWITCH, GPIO.HIGH)
        time.sleep(0.1)
        value = float(self.mcp.read_adc(0))
        #        print("The soil moisture reading is currently at {:.2f}%").format(value / 1023 * 100)
        #        GPIO.output(SWITCH, GPIO.LOW)
        return value

    def collector(self):
        print('Start collecting moisture data')
        try:

            while True:
                value = self.read()
                print('moisture value: ', value)
                self.mqtt_client.publish_sensor_data("moisture", value)
                sleep(Moisture.DELAY_INTERVAL)
        except:
            GPIO.cleanup()

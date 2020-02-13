#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from mqtt_publisher import Publisher
import getpass


class LDR:
    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler
    SPICLK = 11
    SPIMISO = 9
    SPIMOSI = 10
    SPICS = 8
    DELAY_INTERVAL = 2
    TOPIC = 'sensor/light/'

    def __init__(self):

        # photoresistor connected to adc #0
        self.photo_ch = 1

        GPIO.setwarnings(False)
        GPIO.cleanup()  # clean up at the end of your script
        GPIO.setmode(GPIO.BCM)  # to specify whilch pin numbering system
        # set up the SPI interface pins
        GPIO.setup(LDR.SPIMOSI, GPIO.OUT)
        GPIO.setup(LDR.SPIMISO, GPIO.IN)
        GPIO.setup(LDR.SPICLK, GPIO.OUT)
        GPIO.setup(LDR.SPICS, GPIO.OUT)

        self.publisher = Publisher(self.TOPIC + getpass.getuser())
        self.collector()

    # read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if (adcnum > 7) or (adcnum < 0):
            return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)  # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3  # we only need to send 5 bits here
        for i in range(5):
            if commandout & 0x80:
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1  # first bit is 'null' so drop it
        return adcout

    def collector(self):
        print('start collecting data')
        while True:
            adc_value = self.readadc(self.photo_ch, LDR.SPICLK, LDR.SPIMOSI, LDR.SPIMISO, LDR.SPICS)
            print('adc_value', adc_value)
            self.publisher.publish_sensor_data("ldr", adc_value)
            sleep(LDR.DELAY_INTERVAL)


if __name__ == '__main__':
    ldr = LDR()

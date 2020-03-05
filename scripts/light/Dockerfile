FROM balenalib/rpi-raspbian:latest

ADD light/rgb_light.py /
ADD mqtt_subscriber.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install adafruit-circuitpython-neopixel
RUN pip3 install adafruit-blinka
RUN pip3 install rpi_ws281x
RUN pip3 install paho-mqtt
RUN pip3 install Adafruit_MCP3008
#RUN pip3 isntall spidev

ENTRYPOINT ["python3", "-u", "/rgb_light.py"]

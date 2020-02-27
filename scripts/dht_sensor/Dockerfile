FROM balenalib/rpi-raspbian:latest

ADD dht_sensor/dht.py /
ADD mqtt_publisher.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install Adafruit_DHT
RUN pip3 install RPi.GPIO
RUN pip3 install paho-mqtt

ENTRYPOINT ["python3", "-u", "/dht.py"]

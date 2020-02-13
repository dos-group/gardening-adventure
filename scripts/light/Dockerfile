FROM hypriot/wiringpi:latest

ADD rgb_light.py /
ADD ../mqtt_subscriber.py /
ADD /ws2812.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install paho-mqtt
RUN pip3 isntall spidev

ENTRYPOINT ["python3", "-u", "/rgb_light.py"]

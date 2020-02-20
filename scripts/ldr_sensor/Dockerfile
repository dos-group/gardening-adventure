FROM balenalib/rpi-raspbian:latest

ADD ldr.py /
ADD mqtt_publisher.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install RPi.GPIO
RUN pip3 install paho-mqtt

ENTRYPOINT ["python3", "-u", "ldr.py"]

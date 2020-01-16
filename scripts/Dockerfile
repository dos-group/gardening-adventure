FROM hypriot/wiringpi:latest

ADD waterlevel.py /
ADD mqtt_client.py /

RUN apt update
RUN apt-get install python3
RUN apt-get install python3-pip
RUN apt-get install python3-dev

RUN pip3 install RPi.GPIO
RUN pip3 install paho-mqtt

ENTRYPOINT ["python3", "-u", "/waterlevel.py"]
